from PyQt5 import QtWidgets

# Core utility and services
from app.utils.clean_cache import remove_directories
from app.services.image_service import ImageServices
from app.processing.harris import HarrisService

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

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.srv = ImageServices()
        self.harris_srv = HarrisService()

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
        self.ui.harris_threshold_slider.valueChanged.connect(self.update_harris_parameters)
        self.ui.harris_kernel_size_button.clicked.connect(self.update_harris_parameters)

    def drawImage(self):
        self.path = self.srv.upload_image_file()

        # Check if user cancels file selection right after upload attempt
        if not self.path:
            return

        self.original_image = cv2.imread(self.path)
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()

        # Clear any existing images displayed in the group boxes
        self.srv.clear_image(self.ui.original_groupBox)
        self.srv.clear_image(self.ui.processed_groupBox)

        # Display the images in their respective group boxes
        self.srv.set_image_in_groupbox(self.ui.original_groupBox, self.original_image)
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
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing

        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def detect_harris_corners(self):
        """Detect corners using Harris corner detector."""
        if self.original_image is None:
            return

        # Detect corners and get visualization
        harris_corners, hessian_corners, time = self.harris_srv.detect_corners(self.original_image)

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
            print(time)

    def update_harris_parameters(self):
        """Update Harris detector parameters based on slider values."""
        k = 0.04
        threshold = self.ui.harris_threshold_slider.value() /100
        window_size = self.ui.current_kernal_size

        self.harris_srv.update_parameters(k=k, threshold=threshold, window_size=window_size)
        print(threshold, window_size)

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
