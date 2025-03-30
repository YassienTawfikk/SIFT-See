from PyQt5 import QtWidgets

# Core utility and services
from app.utils.clean_cache import remove_directories
from app.services.image_service import ImageServices

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

    def drawImage(self):
        self.path = self.srv.upload_image_file()
        self.original_image = cv2.imread(self.path)
        self.processed_image = self.original_image.copy()

        # If user cancels file selection, path could be None
        if self.path:
            self.srv.clear_image(self.ui.original_groupBox)
            self.srv.clear_image(self.ui.processed_groupBox)
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

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
