from PyQt5 import QtWidgets

# Core utility and services
from app.utils.clean_cache import remove_directories
from app.utils.logging_manager import LoggingManager
from app.services.image_service import ImageServices
from app.processing.harris import HarrisService
from app.processing.sift import SIFTService

# Main GUI design
from app.design.main_layout import Ui_MainWindow

# Image processing functionality
import cv2


class MainWindowController:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()

        self.path = None
        self.path_1 = None
        self.path_2 = None

        self.original_image = None
        self.processed_image = None
        self.second_image = None
        self.keypoints_1 = None
        self.descriptors_1 = None
        self.keypoints_2 = None
        self.descriptors_2 = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.log = LoggingManager()

        self.srv = ImageServices()
        self.harris_srv = HarrisService()
        self.sift_srv = SIFTService()

        # Connect signals to slots
        self.setupConnections()

    def run(self):
        """Run the application."""
        self.MainWindow.showFullScreen()
        self.app.exec_()

    def setupConnections(self):
        """Connect buttons to their respective methods."""
        self.ui.quit_app_button.clicked.connect(self.closeApp)
        self.ui.upload_button.clicked.connect(self.drawImage)

        self.ui.save_image_button.clicked.connect(lambda: self.srv.save_image(self.processed_image))

        self.ui.clear_image_button.clicked.connect(self.clear_images)
        self.ui.reset_image_button.clicked.connect(self.reset_images)

        # Harris corner detection connections
        self.ui.harris_operator_apply_button.clicked.connect(self.detect_harris_corners)
        self.ui.lambda_harris_operator_apply_button.clicked.connect(self.detect_lambda_corners)
        self.ui.harris_threshold_slider.valueChanged.connect(self.update_harris_parameters)
        self.ui.harris_kernel_size_button.clicked.connect(self.update_harris_parameters)

        # SIFT connections
        self.ui.sift_sigma_slider.valueChanged.connect(self.update_sift_parameters)
        self.ui.sift_k_spinbox.valueChanged.connect(self.update_sift_parameters)
        self.ui.sift_constant_threshold_spinbox.valueChanged.connect(self.update_sift_parameters)
        self.ui.sift_edge_threshold_spinbox.valueChanged.connect(self.update_sift_parameters)
        # self.ui.sift_magnitude_threshold_spinbox.valueChanged.connect(self.update_sift_parameters)
        self.ui.upload_sift_photo_button.clicked.connect(self.upload_second_image)
        self.ui.sift_extract_points_button.clicked.connect(self.extract_sift_features)
        self.ui.sift_match_button.clicked.connect(self.match_sift_features)

    def drawImage(self):
        self.path = self.srv.upload_image_file()

        if not self.path:
            return

        self.original_image = cv2.imread(self.path)
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()

        # Clear any existing images
        self.srv.clear_image(self.ui.original_groupBox)
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.clear_image(self.ui.additional_groupBox)

        # Display the original image in the bottom-left box
        self.srv.set_image_in_groupbox(self.ui.original_groupBox, self.original_image)
        
        # Initially show the same image in the large processed box
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def clear_images(self):
        if self.original_image is None:
            return

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.clear_image(self.ui.original_groupBox)

    def reset_images(self):
        if self.original_image is None:
            return

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.original_image)

    def showProcessed(self):
        """Display the processed image in the large top box."""
        if self.processed_image is None:
            return

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def detect_harris_corners(self):
        """Detect corners using Harris corner detector."""
        if self.original_image is None:
            return

        # Detect corners and get visualization
        harris_corners, time = self.harris_srv.detect_harris_corners(self.original_image)

        if harris_corners is not None:
            # Update processed image with visualization
            # Create a copy of the original image to draw corners
            self.processed_image = self.original_image.copy()

            # Draw red circles at the detected corners
            for y in range(harris_corners.shape[0]):
                for x in range(harris_corners.shape[1]):
                    if harris_corners[y, x]:  # If a corner is detected
                        cv2.circle(self.processed_image, (x, y), 5, (255, 0, 0), -1)

            self.showProcessed()
            self.log.log(time)

    def detect_lambda_corners(self):
        """Detect corners using Harris corner detector."""
        if self.original_image is None:
            return

        # Detect corners and get visualization
        hessian_corners, time = self.harris_srv.detect_lambda_corners(self.original_image)

        if hessian_corners is not None:
            # Update processed image with visualization
            # Create a copy of the original image to draw corners
            self.processed_image = self.original_image.copy()

            # Draw red circles at the detected corners
            for y in range(hessian_corners.shape[0]):
                for x in range(hessian_corners.shape[1]):
                    if hessian_corners[y, x]:  # If a corner is detected
                        cv2.circle(self.processed_image, (x, y), 5, (255, 0, 0), -1)

            self.showProcessed()
            self.log.log(time)

    def update_harris_parameters(self):
        """Update Harris detector parameters based on slider values."""
        k = 0.04
        threshold = self.ui.harris_threshold_slider.value() / 100
        window_size = self.ui.current_kernal_size

        self.harris_srv.update_parameters(k=k, threshold=threshold, window_size=window_size)
        print(threshold, window_size)

    def update_sift_parameters(self):
        """Update SIFT parameters based on UI control values."""
        sigma = self.ui.sift_sigma_slider.value() / 2.0  # Scale to 0.5-5.0 range
        k = self.ui.sift_k_spinbox.value()
        constant_threshold = self.ui.sift_constant_threshold_spinbox.value() / 100.0
        edge_threshold = self.ui.sift_edge_threshold_spinbox.value()
        # magnitude_threshold = self.ui.sift_magnitude_threshold_spinbox.value() / 100.0

        self.sift_srv.update_parameters(
            sigma=sigma,
            k=k,
            constant_threshold=constant_threshold,
            edge_threshold=edge_threshold,
            # magnitude_threshold=magnitude_threshold
        )

    def upload_second_image(self):
        """Upload a second image for SIFT matching."""
        self.path_2 = self.srv.upload_image_file()
        if not self.path_2:
            return

        self.second_image = cv2.imread(self.path_2)
        if self.second_image is None:
            return

        # Display the second image in the bottom-right box
        self.srv.clear_image(self.ui.additional_groupBox)
        self.srv.set_image_in_groupbox(self.ui.additional_groupBox, self.second_image)

    def extract_sift_features(self):
        """Extract SIFT features from both images."""
        if self.original_image is None:
            return

        # Extract features from the first image
        self.keypoints_1, self.descriptors_1, time = self.sift_srv.extract_features(self.original_image)
        
        # Create visualization for first image
        img1_with_keypoints = self.sift_srv.draw_keypoints(self.original_image.copy(), self.keypoints_1)
        
        if self.second_image is not None:
            # Extract features from second image
            self.keypoints_2, self.descriptors_2, _ = self.sift_srv.extract_features(self.second_image)
            img2_with_keypoints = self.sift_srv.draw_keypoints(self.second_image.copy(), self.keypoints_2)
            
            # Get dimensions
            h1, w1 = img1_with_keypoints.shape[:2]
            h2, w2 = img2_with_keypoints.shape[:2]
            
            # Calculate target height (use the smaller height)
            target_height = min(h1, h2)
            
            # Calculate new widths maintaining aspect ratio
            new_w1 = int(w1 * (target_height / h1))
            new_w2 = int(w2 * (target_height / h2))
            
            # Resize both images to have the same height
            img1_resized = cv2.resize(img1_with_keypoints, (new_w1, target_height))
            img2_resized = cv2.resize(img2_with_keypoints, (new_w2, target_height))
            
            # Create a combined image with both visualizations
            combined_image = cv2.hconcat([img1_resized, img2_resized])
            
            # Show the combined visualization in the large processed box
            self.processed_image = combined_image
            self.showProcessed()
        else:
            # If no second image, just show the first image with keypoints
            self.processed_image = img1_with_keypoints
            self.showProcessed()
            
        self.log.log(time)

    def match_sift_features(self):
        """Match SIFT features between two images."""
        if (self.descriptors_1 is None or self.descriptors_2 is None or 
            self.keypoints_1 is None or self.keypoints_2 is None):
            return

        # Get the size of the processed group box
        box_width = self.ui.processed_groupBox.width()
        box_height = self.ui.processed_groupBox.height()
        
        # Calculate target size for each image (half width, full height)
        target_width = box_width // 2
        target_height = box_height
        
        # Resize both images while maintaining aspect ratio
        def resize_image(image):
            h, w = image.shape[:2]
            # Calculate scaling factor to fit in half the box
            scale_w = target_width / w
            scale_h = target_height / h
            scale = min(scale_w, scale_h)
            
            new_width = int(w * scale)
            new_height = int(h * scale)
            
            return cv2.resize(image, (new_width, new_height))
        
        # Resize both images
        img1_resized = resize_image(self.original_image)
        img2_resized = resize_image(self.second_image)
        
        # Update keypoints for resized images
        def adjust_keypoints(keypoints, original_shape, new_shape):
            scale_x = new_shape[1] / original_shape[1]
            scale_y = new_shape[0] / original_shape[0]
            
            adjusted_keypoints = []
            for kp in keypoints:
                new_kp = cv2.KeyPoint(
                    x=kp.pt[0] * scale_x,
                    y=kp.pt[1] * scale_y,
                    size=kp.size * min(scale_x, scale_y),
                    angle=kp.angle,
                    response=kp.response,
                    octave=kp.octave,
                    class_id=kp.class_id
                )
                adjusted_keypoints.append(new_kp)
            return adjusted_keypoints
        
        # Adjust keypoints for the resized images
        keypoints1_adjusted = adjust_keypoints(
            self.keypoints_1, 
            self.original_image.shape, 
            img1_resized.shape
        )
        keypoints2_adjusted = adjust_keypoints(
            self.keypoints_2, 
            self.second_image.shape, 
            img2_resized.shape
        )

        # Match features
        matches = self.sift_srv.match_features(self.descriptors_1, self.descriptors_2)
        
        # Draw matches using the resized images and adjusted keypoints
        self.processed_image = self.sift_srv.draw_matches(
            img1_resized, keypoints1_adjusted,
            img2_resized, keypoints2_adjusted,
            matches
        )
        
        # Show the result
        self.showProcessed()

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
