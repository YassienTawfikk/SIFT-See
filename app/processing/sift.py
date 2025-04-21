import cv2
import numpy as np
from typing import Tuple, List, Optional
from scipy.ndimage import gaussian_filter
import time


class SIFTService:
    def __init__(self):
        self.sigma = 1.6  # Base sigma
        self.k = 2  # Scale multiplier between levels
        self.num_octaves = 4  # Number of octaves
        self.num_scales = 5  # Number of scales per octave
        #keypoint detection
        self.contrast_threshold = 0.04  # Contrast threshold
        self.edge_threshold = 10.0  # Edge threshold

        
    def update_parameters(self, sigma: float = None, k: int = None,
                         contrast_threshold: float = None, edge_threshold: float = None):
        """Update SIFT parameters."""
        if sigma is not None:
            self.sigma = sigma
        if k is not None:
            self.k = k
        if contrast_threshold is not None:
            self.contrast_threshold = contrast_threshold
        if edge_threshold is not None:
            self.edge_threshold = edge_threshold

    def build_gaussian_pyramid(self, image: np.ndarray) -> List[List[np.ndarray]]:
        """
        creates a pyramid structure where each octave represents a different resolution level
        for every Octave we get different Scales (apply gaussian blur)/ blurred images
        Returns list of octaves, each containing gaussian blurred images.
        """

        image = image.astype('float32')

        pyramid = []

        for octave in range(self.num_octaves): # Octave = Resolution (row)
            octave_images = []

            # Downsample image for each octave -> halving resolution
            if octave > 0:
                image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))
            
            # Generate "scales" for this octave
            current_sigma = self.sigma
            for scale in range(self.num_scales):
                # Applying Gaussian blur with increasing sigma values (σ, σk, σk²,...) at each scale
                blurred = cv2.GaussianBlur(image, (0, 0), current_sigma)
                octave_images.append(blurred)
                current_sigma *= self.k
                
            pyramid.append(octave_images)
            
        return pyramid

    def build_dog_pyramid(self, gaussian_pyramid: List[List[np.ndarray]]) -> List[List[np.ndarray]]:
        """
        computes differences between consecutive Gaussian blurred images in same octave (in the same row)
        approximation to the Laplacian of Gaussian
        Returns list of octaves, each containing DoG images.
        """
        dog_pyramid = []
        
        for octave_images in gaussian_pyramid:
            dog_octave = []
            for i in range(len(octave_images) - 1):
                # Compute difference of consecutive Gaussian blurred images
                dog = octave_images[i+1] - octave_images[i]
                dog_octave.append(dog) # DoG for every octave
            dog_pyramid.append(dog_octave)
            
        return dog_pyramid

    def find_keypoints(self, dog_pyramid: List[List[np.ndarray]]) -> List[cv2.KeyPoint]:
        keypoints = []
        # print("initial parameters : " , self.sigma , self.k, self.contrast_threshold, self.edge_threshold)
        for octave_idx, octave in enumerate(dog_pyramid):
            for scale_idx in range(1, len(octave) - 1):
                prev, current, next = octave[scale_idx - 1:scale_idx + 2]

                # Pad images to handle borders
                pad = [(1, 1)] * 2
                prev_pad = np.pad(prev, pad, 'constant')
                curr_pad = np.pad(current, pad, 'constant')
                next_pad = np.pad(next, pad, 'constant')

                h, w = current.shape
                for i in range(1, h - 1):
                    for j in range(1, w - 1):
                        val = current[i, j]
                        if abs(val) <= self.contrast_threshold:
                            continue

                        # Check 3x3x3 neighborhood
                        cube = np.stack([
                            prev_pad[i:i + 3, j:j + 3],
                            curr_pad[i:i + 3, j:j + 3],
                            next_pad[i:i + 3, j:j + 3]
                        ])

                        is_max = val > 0 and val >= cube.max()
                        is_min = val < 0 and val <= cube.min()
                        if not (is_max or is_min):
                            continue

                        # H = [ Dxx  Dxy ]
                        #     [ Dxy  Dyy ]

                        # Edge response check , Hessian matrix components (Dxx, Dyy, Dxy)
                        Dxx = current[i, j + 1] + current[i, j - 1] - 2 * val
                        Dyy = current[i + 1, j] + current[i - 1, j] - 2 * val
                        Dxy = (current[i + 1, j + 1] + current[i - 1, j - 1] -
                               current[i + 1, j - 1] - current[i - 1, j + 1]) / 4

                        trace, det = Dxx + Dyy, Dxx * Dyy - Dxy * Dxy
                        edge_ratio = (self.edge_threshold + 1) ** 2 / self.edge_threshold
                        if det <= 0 or trace ** 2 / det >= edge_ratio: #Filters edge responses using curvature ratio: (trace²/det) < threshold
                            continue

                        # Create keypoint
                        kp = cv2.KeyPoint()
                        scale_factor = 2 ** octave_idx      # Stores position scaled by octave factor (2^octave)
                        kp.pt = (j * scale_factor, i * scale_factor)
                        current_sigma = self.sigma * (self.k ** scale_idx)
                        kp.size = current_sigma * scale_factor  # scale_factor = 2^octave_idx
                        kp.octave = octave_idx
                        keypoints.append(kp)

        return keypoints[:500]

    def compute_descriptors(self, image: np.ndarray, keypoints: List[cv2.KeyPoint]) -> np.ndarray:
        if not keypoints:
            return np.array([])

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
        # Computes x/y gradients
        dx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        dy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)

        magnitude = np.sqrt(dx ** 2 + dy ** 2)
        orientation = np.rad2deg(np.arctan2(dy, dx)) % 360

        descriptors = []
        for kp in keypoints:
            x, y = map(int, kp.pt)
            scale = kp.size / self.sigma
            radius = int(6 * scale)

            # Check boundary conditions
            if (x < radius or x + radius >= gray.shape[1] or
                    y < radius or y + radius >= gray.shape[0]):
                continue

            # Extract and resize patches
            patch = (slice(y - radius, y + radius + 1), slice(x - radius, x + radius + 1))
            # Extracts 16x16 patch around keypoint (scaled by feature size)
            mag_patch = cv2.resize(magnitude[patch], (16, 16))
            ori_patch = cv2.resize(orientation[patch], (16, 16))

            # Build histogram
            hist = np.zeros(128, dtype=np.float32)

            for i in range(4):
                for j in range(4):
                    cell_mag = mag_patch[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4]
                    cell_ori = ori_patch[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4]

                    # Each cell creates 8-bin orientation histogram (0-360°)
                    for bin in range(8):
                        mask = (cell_ori >= bin * 45) & (cell_ori < (bin + 1) * 45)
                        hist[i * 32 + j * 8 + bin] = cell_mag[mask].sum()

            # Normalize descriptor
            hist /= np.linalg.norm(hist) + 1e-7
            hist = np.clip(hist, 0, 0.2)
            hist /= np.linalg.norm(hist) + 1e-7

            descriptors.append(hist)

        return np.array(descriptors)

    def extract_features(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray, float]:
        """
        Extract SIFT features from an image.
        Returns keypoints, descriptors, and computation time.
        """
        start_time = time.time()

        # Convert to grayscale if needed
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

        # 1) Build Gaussian pyramid
        gaussian_pyramid = self.build_gaussian_pyramid(gray)

        # 2) Build DoG pyramid
        dog_pyramid = self.build_dog_pyramid(gaussian_pyramid)

        # 3) Find keypoints
        keypoints = self.find_keypoints(dog_pyramid)

        # 4) Compute descriptors
        descriptors = self.compute_descriptors(image, keypoints)

        computation_time = time.time() - start_time
        print(computation_time)

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

    def match_features(self, descriptors1: np.ndarray, descriptors2: np.ndarray, method="SSD") -> list:
        """Match features using SSD or Normalized Cross Correlation"""
        if len(descriptors1) == 0 or len(descriptors2) == 0:
            return []

        matches = []
        SSD_threshold=100
        NNC_threshold=0.8

        for i, desc1 in enumerate(descriptors1):

            if method=="SSD":
                print("SSD METHOD USED")

                # Compute SSD to every descriptor in descriptors2
                ssd = np.sum((descriptors2 - desc1) ** 2, axis=1)

                # Get the index of the descriptor in descriptors2 with the smallest SSD
                j = np.argmin(ssd)

                # Store the match (i, j)
                distance = ssd[j]

                if distance > SSD_threshold:
                    continue

                # Create a DMatch object: (queryIdx, trainIdx, distance)
                match = cv2.DMatch(_queryIdx=i, _trainIdx=j, _distance=float(distance))

            else:  #method is NNC
                print("NNC METHOD USED")

                # Normalize descriptor1
                norm1 = desc1 / (np.linalg.norm(desc1) + 1e-10)

                # Normalize all descriptors2
                norm2 = descriptors2 / (np.linalg.norm(descriptors2, axis=1, keepdims=True) + 1e-10)

                # Compute NCC as dot product
                ncc_scores = norm2 @ norm1  # shape: (N2,)

                # Get best match (maximum NCC)
                j = np.argmax(ncc_scores)
                similarity = ncc_scores[j]

                if similarity < NNC_threshold:
                    continue 

                # Create a DMatch object (higher NCC = better match, so use -similarity for distance)
                match = cv2.DMatch(_queryIdx=i, _trainIdx=j, _distance=float(-similarity))


            matches.append(match)
            # print(match)
            # for m in matches[:10]:  # just print first 10 to keep it clean
            #     print(f"queryIdx: {m.queryIdx}, trainIdx: {m.trainIdx}, distance: {m.distance:.2f}")
        return matches

    def draw_matches(self, img1: np.ndarray, kp1: list, img2: np.ndarray,
                    kp2: list, matches: list) -> np.ndarray:
        """Draw matches between two images."""
        return cv2.drawMatches(
            img1, kp1, img2, kp2, matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )