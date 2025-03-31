import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class HarrisService:
    def __init__(self):
        self.k = 0.04  # Harris detector free parameter
        self.threshold = 0.01  # Threshold for corner detection
        self.window_size = 3  # Window size for Gaussian smoothing

    def detect_corners(self, image):
        """
        Detect corners using Harris corner detector and analyze eigenvalues

        Args:
            image: Input image (numpy array)

        Returns:
            tuple: (corners, eigenvalues, visualization)
        """
        if image is None:
            return None, None, None

        # Convert to grayscale if image is color
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Calculate derivatives
        dy, dx = np.gradient(gray)

        # Calculate products of derivatives
        Ixx = dx ** 2
        Ixy = dy * dx
        Iyy = dy ** 2

        # Apply Gaussian window
        kernel = np.ones((self.window_size, self.window_size), np.float32) / (self.window_size ** 2)
        Sxx = cv2.filter2D(Ixx, -1, kernel)
        Sxy = cv2.filter2D(Ixy, -1, kernel)
        Syy = cv2.filter2D(Iyy, -1, kernel)

        # Calculate Harris matrix eigenvalues
        det = (Sxx * Syy) - (Sxy ** 2)
        trace = Sxx + Syy
        harris_response = det - self.k * (trace ** 2)

        # Find corners
        corners = harris_response > (self.threshold * harris_response.max())


        return corners


    def update_parameters(self, k=None, threshold=None, window_size=None):
        """
        Update the Harris detector parameters

        Args:
            k: Harris detector free parameter
            threshold: Threshold for corner detection
            window_size: Window size for Gaussian smoothing
        """
        if k is not None:
            self.k = k
        if threshold is not None:
            self.threshold = threshold
        if window_size is not None:
            self.window_size = window_size

