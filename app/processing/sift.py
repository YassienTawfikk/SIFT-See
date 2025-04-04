import cv2
import numpy as np
from typing import Tuple, List, Optional
from scipy.ndimage import gaussian_filter


class SIFTService:
    def __init__(self):
        self.sigma = 1.6  # Base sigma
        self.k = 2  # Number of scales per octave
        self.constant_threshold = 0.04  # Contrast threshold
        self.edge_threshold = 10.0  # Edge threshold
        self.num_octaves = 4  # Number of octaves
        self.num_scales = 5  # Number of scales per octave
        
    def update_parameters(self, sigma: float = None, k: int = None, 
                         constant_threshold: float = None, edge_threshold: float = None):
        """Update SIFT parameters."""
        if sigma is not None:
            self.sigma = sigma
        if k is not None:
            self.k = k
        if constant_threshold is not None:
            self.constant_threshold = constant_threshold
        if edge_threshold is not None:
            self.edge_threshold = edge_threshold

    def build_gaussian_pyramid(self, image: np.ndarray) -> List[List[np.ndarray]]:
        """
        Build Gaussian pyramid for the image.
        Returns list of octaves, each containing gaussian blurred images.
        """
        # Convert to float32
        image = image.astype('float32')
        
        # Initialize pyramid
        pyramid = []
        
        for octave in range(self.num_octaves):
            octave_images = []
            
            # Downsample image for each octave
            if octave > 0:
                image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))
            
            # Generate scales for this octave
            current_sigma = self.sigma
            for scale in range(self.num_scales):
                # Apply Gaussian blur
                blurred = cv2.GaussianBlur(image, (0, 0), current_sigma)
                octave_images.append(blurred)
                current_sigma *= self.k
                
            pyramid.append(octave_images)
            
        return pyramid

    def build_dog_pyramid(self, gaussian_pyramid: List[List[np.ndarray]]) -> List[List[np.ndarray]]:
        """
        Build Difference of Gaussian (DoG) pyramid.
        Returns list of octaves, each containing DoG images.
        """
        dog_pyramid = []
        
        for octave_images in gaussian_pyramid:
            dog_octave = []
            for i in range(len(octave_images) - 1):
                # Compute difference of consecutive Gaussian blurred images
                dog = octave_images[i+1] - octave_images[i]
                dog_octave.append(dog)
            dog_pyramid.append(dog_octave)
            
        return dog_pyramid

    def find_keypoints(self, dog_pyramid: List[List[np.ndarray]]) -> List[cv2.KeyPoint]:
        """
        Detect keypoints in the DoG pyramid using vectorized operations.
        Returns list of keypoints.
        """
        keypoints = []
        
        for octave_idx, dog_octave in enumerate(dog_pyramid):
            for scale_idx in range(1, len(dog_octave) - 1):
                # Get current DoG image and its neighbors
                current = dog_octave[scale_idx]
                prev = dog_octave[scale_idx - 1]
                next = dog_octave[scale_idx + 1]
                
                # Create 3D array of local patches
                height, width = current.shape
                window_size = 3
                
                # Pad images to handle borders
                current_pad = np.pad(current, 1, mode='constant')
                prev_pad = np.pad(prev, 1, mode='constant')
                next_pad = np.pad(next, 1, mode='constant')
                
                # Find local extrema
                maxima = np.zeros_like(current, dtype=bool)
                minima = np.zeros_like(current, dtype=bool)
                
                # Vectorized extrema detection
                for i in range(1, height-1):
                    for j in range(1, width-1):
                        # Extract 3x3x3 cube
                        cube = np.stack([
                            prev_pad[i:i+3, j:j+3],
                            current_pad[i:i+3, j:j+3],
                            next_pad[i:i+3, j:j+3]
                        ])
                        
                        center_val = current[i, j]
                        if abs(center_val) > self.constant_threshold:
                            if center_val > 0 and center_val >= cube.max():
                                # Edge response test
                                Dxx = current[i, j+1] + current[i, j-1] - 2*center_val
                                Dyy = current[i+1, j] + current[i-1, j] - 2*center_val
                                Dxy = ((current[i+1, j+1] + current[i-1, j-1]) - 
                                      (current[i+1, j-1] + current[i-1, j+1])) / 4
                                
                                tr = Dxx + Dyy
                                det = Dxx * Dyy - Dxy * Dxy
                                
                                if det > 0 and tr*tr/det < (self.edge_threshold + 1)**2/self.edge_threshold:
                                    kp = cv2.KeyPoint()
                                    scale_factor = 2**octave_idx
                                    kp.pt = (j * scale_factor, i * scale_factor)
                                    kp.size = self.sigma * (2**(scale_idx/self.num_scales)) * scale_factor
                                    kp.octave = octave_idx
                                    keypoints.append(kp)
                            elif center_val < 0 and center_val <= cube.min():
                                # Edge response test
                                Dxx = current[i, j+1] + current[i, j-1] - 2*center_val
                                Dyy = current[i+1, j] + current[i-1, j] - 2*center_val
                                Dxy = ((current[i+1, j+1] + current[i-1, j-1]) - 
                                      (current[i+1, j-1] + current[i-1, j+1])) / 4
                                
                                tr = Dxx + Dyy
                                det = Dxx * Dyy - Dxy * Dxy
                                
                                if det > 0 and tr*tr/det < (self.edge_threshold + 1)**2/self.edge_threshold:
                                    kp = cv2.KeyPoint()
                                    scale_factor = 2**octave_idx
                                    kp.pt = (j * scale_factor, i * scale_factor)
                                    kp.size = self.sigma * (2**(scale_idx/self.num_scales)) * scale_factor
                                    kp.octave = octave_idx
                                    keypoints.append(kp)
        
        return keypoints[:500]  # Limit number of keypoints for better performance

    def compute_descriptors(self, image: np.ndarray, keypoints: List[cv2.KeyPoint]) -> np.ndarray:
        """
        Compute SIFT descriptors using vectorized operations.
        Returns array of descriptors.
        """
        if not keypoints:
            return np.array([])

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Pre-compute gradients for the entire image
        dx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        dy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        
        # Pre-compute magnitude and orientation
        magnitude = np.sqrt(dx*dx + dy*dy)
        orientation = np.arctan2(dy, dx) * 180/np.pi
        orientation[orientation < 0] += 360  # Ensure positive angles
        
        descriptors = []
        patch_size = 16  # Fixed patch size for all keypoints
        
        # Process keypoints in batches for better performance
        batch_size = min(50, len(keypoints))
        for batch_start in range(0, len(keypoints), batch_size):
            batch_end = min(batch_start + batch_size, len(keypoints))
            batch_keypoints = keypoints[batch_start:batch_end]
            
            batch_descriptors = []
            for kp in batch_keypoints:
                x, y = int(kp.pt[0]), int(kp.pt[1])
                scale = kp.size/self.sigma
                radius = int(6 * scale)
                
                if (x - radius < 0 or x + radius >= gray.shape[1] or 
                    y - radius < 0 or y + radius >= gray.shape[0]):
                    continue
                
                # Extract and resize patches
                patch_mag = cv2.resize(magnitude[y-radius:y+radius+1, x-radius:x+radius+1], 
                                    (patch_size, patch_size))
                patch_ori = cv2.resize(orientation[y-radius:y+radius+1, x-radius:x+radius+1], 
                                    (patch_size, patch_size))
                
                # Compute descriptor using vectorized operations
                hist = np.zeros(128, dtype=np.float32)
                for i in range(4):
                    for j in range(4):
                        cell_mag = patch_mag[i*4:(i+1)*4, j*4:(j+1)*4]
                        cell_ori = patch_ori[i*4:(i+1)*4, j*4:(j+1)*4]
                        
                        # Compute histogram using vectorized operations
                        for bin_idx in range(8):
                            angle_start = bin_idx * 45
                            angle_end = (bin_idx + 1) * 45
                            mask = (cell_ori >= angle_start) & (cell_ori < angle_end)
                            hist[i*32 + j*8 + bin_idx] = np.sum(cell_mag[mask])
                
                # Normalize and clip
                norm = np.sqrt(np.sum(hist * hist) + 1e-7)
                hist = np.minimum(hist / norm, 0.2)
                norm = np.sqrt(np.sum(hist * hist) + 1e-7)
                hist = hist / norm
                
                batch_descriptors.append(hist)
            
            descriptors.extend(batch_descriptors)
        
        return np.array(descriptors)

    def extract_features(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray, float]:
        """
        Extract SIFT features from an image.
        Returns keypoints, descriptors, and computation time.
        """
        import time
        start_time = time.time()

        # Convert to grayscale if needed
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Build Gaussian pyramid
        gaussian_pyramid = self.build_gaussian_pyramid(gray)
        
        # Build DoG pyramid
        dog_pyramid = self.build_dog_pyramid(gaussian_pyramid)
        
        # Find keypoints
        keypoints = self.find_keypoints(dog_pyramid)
        
        # Compute descriptors
        descriptors = self.compute_descriptors(image, keypoints)

        computation_time = time.time() - start_time
        
        return keypoints, descriptors, computation_time

    def draw_keypoints(self, image: np.ndarray, keypoints: list) -> np.ndarray:
        """Draw keypoints on the image."""
        return cv2.drawKeypoints(
            image, 
            keypoints, 
            None,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
            color=(0, 255, 0)
        )

    def match_features(self, descriptors1: np.ndarray, descriptors2: np.ndarray, 
                      ratio_threshold: float = 0.75) -> list:
        """Match features using vectorized operations."""
        if len(descriptors1) == 0 or len(descriptors2) == 0:
            return []
            
        # Use batch processing for large descriptor sets
        batch_size = 100
        matches = []
        
        for i in range(0, len(descriptors1), batch_size):
            batch_desc1 = descriptors1[i:i + batch_size]
            
            # Compute distances using broadcasting
            distances = np.linalg.norm(
                batch_desc1[:, np.newaxis, :] - descriptors2[np.newaxis, :, :], 
                axis=2
            )
            
            # Find two best matches
            idx = np.argsort(distances, axis=1)
            best_dists = distances[np.arange(len(batch_desc1)), idx[:, 0]]
            second_dists = distances[np.arange(len(batch_desc1)), idx[:, 1]]
            
            # Apply ratio test
            good_matches = best_dists < ratio_threshold * second_dists
            
            # Create match objects
            for k in range(len(batch_desc1)):
                if good_matches[k]:
                    match = cv2.DMatch()
                    match.queryIdx = i + k
                    match.trainIdx = idx[k, 0]
                    match.distance = best_dists[k]
                    matches.append(match)
        
        return matches[:100]  # Limit number of matches for visualization

    def draw_matches(self, img1: np.ndarray, kp1: list, img2: np.ndarray, 
                    kp2: list, matches: list) -> np.ndarray:
        """Draw matches between two images."""
        return cv2.drawMatches(
            img1, kp1, img2, kp2, matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        ) 