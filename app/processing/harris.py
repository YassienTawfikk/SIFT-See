import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import time  # Importing the time module


class HarrisService:
    def _init_(self):
        self.k = 0.04  # Harris detector free parameter
        self.threshold = 0.01  # Threshold for corner detection
        self.window_size = 3  # Window size for Gaussian smoothing

    def detect_corners(self, image):
        """
        Detect corners using both Harris corner detector and Hessian matrix eigenvalues

        Args:
            image: Input image (numpy array)

        Returns:
            tuple: (harris_corners, hessian_corners, computation_time)
        """
        if image is None:
            return None, None, None

        # Start timing
        start_time = time.time()

        # Convert to grayscale if image is color
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # 1. Harris Corner Detection
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

        # Find Harris corners
        harris_corners = harris_response > (self.threshold * harris_response.max())

        # 2. Hessian Matrix Corner Detection
        # Calculate second derivatives
        dyy, dyx = np.gradient(dy)
        dxy, dxx = np.gradient(dx)

        # Apply Gaussian window to second derivatives
        dxx = cv2.filter2D(dxx, -1, kernel)
        dxy = cv2.filter2D(dxy, -1, kernel)
        dyy = cv2.filter2D(dyy, -1, kernel)

        # Calculate eigenvalues of Hessian matrix
        trace = dxx + dyy
        det = dxx * dyy - dxy * dxy

        # Calculate negative eigenvalues
        lambda2 = (trace - np.sqrt(trace ** 2 - 4 * det)) / 2

        # Find corners where both eigenvalues are negative
        hessian_corners = (lambda2 >self.threshold)

        # End timing
        computation_time = time.time() - start_time

        return harris_corners, hessian_corners, computation_time

    def update_parameters(self, k=None, threshold=None, window_size=None):
        """
        Update the corner detector parameters

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