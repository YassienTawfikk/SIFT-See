from PyQt5 import QtCore, QtGui, QtWidgets
from app.design.tools.gui_utilities import GUIUtilities


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.screen_size = QtWidgets.QApplication.primaryScreen().size()
        MainWindow.resize(self.screen_size.width(), self.screen_size.height())

        # 1) Define style variables
        self.setupStyles()
        self.util = GUIUtilities()

        # 2) Apply main window style
        MainWindow.setStyleSheet(self.main_window_style)

        # 3) Central widget & main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.main_vertical_layout.setSpacing(0)

        # 4) Create Title (icon + label) and Navbar (upload, reset, save, quit)
        self.setupTitleArea()
        self.setupNavbar()
        self.combineTitleAndNavbar()

        # Add the top bar (title+navbar) to the main vertical layout
        self.main_vertical_layout.addLayout(self.title_nav_layout)

        # 5) Create the main content: left sidebar + two group boxes on the right
        self.setupMainContent()
        self.main_vertical_layout.addLayout(self.main_content_layout)

        # 6) Finalize the main window
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar & status bar (if needed)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.original_groupBox.show()
        # self.processed_groupBox.show()

        # 7) Set window title, etc.
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ----------------------------------------------------------------------
    # Styles
    # ----------------------------------------------------------------------
    def setupStyles(self):
        """Holds all style sheets in one place for easier modification."""
        self.main_window_style = "background-color: rgb(30, 0, 0);"
        self.button_style = """
            QPushButton {
                background-color: rgb(0, 0, 0);
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
                border: 1px solid white;
            }
            QPushButton:hover {
                background-color: rgb(30, 10, 10);
            }
        """
        self.quit_button_style = """
            QPushButton {
                color: rgb(255, 255, 255);
                border: 3px solid rgb(255, 255, 255);
            }
            QPushButton:hover {
                border-color: rgb(253, 94, 80);
                color: rgb(253, 94, 80);
            }
        """
        self.groupbox_style = """
            color: white;
            border: 1px solid white;
        """
        self.slider_style = """
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 2px;
            background: #3E0202; /* Dark red, similar to the main window background */
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: rgb(0, 0, 0); /* Black, like the button background */
            width: 16px;
            margin: -10px 0; /* Increase or decrease the vertical margin if the handle seems misaligned */
            border-radius: 3px;
            border: 1px solid white; /* Matching button border */
        }
        QSlider::sub-page:horizontal {
            background: white; /* Dark red, hover color from the button */
            border: 1px solid rgb(30, 10, 10);
            height: 2px;
            border-radius: 2px;
        }
        """

    # ----------------------------------------------------------------------
    # Title + Navbar
    # ----------------------------------------------------------------------
    def setupTitleArea(self):
        """Creates the title icon & label in a horizontal layout."""
        self.title_icon = QtWidgets.QLabel()
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/icons/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")

        self.title_label = self.util.createLabel(
            text="Sift & See",
            style="color:white; padding:10px; padding-left:0;",
            isHead=True
        )
        font = QtGui.QFont()
        font.setFamily("Palatino")
        font.setPointSize(35)
        font.setBold(True)
        font.setItalic(True)
        self.title_label.setFont(font)

        # Horizontal layout for icon + label
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addWidget(self.title_icon)
        self.title_layout.addWidget(self.title_label)

    def setupNavbar(self):
        """Creates the Upload, Reset, Save, and Quit buttons."""
        self.upload_button = self.util.createButton("Upload", self.button_style)
        self.reset_image_button = self.util.createButton("Reset", self.button_style)
        self.save_image_button = self.util.createButton("Save", self.button_style)
        self.clear_image_button = self.util.createButton("Clear", self.button_style)

        self.quit_app_button = self.util.createButton("X")
        self.util.adjust_quit_button(self.quit_app_button)

        self.navbar_layout = QtWidgets.QHBoxLayout()
        self.navbar_layout.setSpacing(25)
        self.navbar_layout.addWidget(self.upload_button)
        self.navbar_layout.addWidget(self.reset_image_button)
        self.navbar_layout.addWidget(self.save_image_button)
        self.navbar_layout.addWidget(self.clear_image_button)
        self.navbar_layout.addWidget(self.quit_app_button)

    def combineTitleAndNavbar(self):
        """Combines the title & navbar in one horizontal layout."""
        self.title_nav_layout = QtWidgets.QHBoxLayout()
        self.title_nav_layout.addLayout(self.title_layout)
        self.title_nav_layout.addStretch(1)
        self.title_nav_layout.addLayout(self.navbar_layout)

    # ----------------------------------------------------------------------
    # Main Content: Sidebar + GroupBoxes
    # ----------------------------------------------------------------------
    def setupMainContent(self):
        """
        Creates a horizontal layout that includes:
         - A stacked sidebar (main buttons vs. noise controls)
         - Two group boxes (Original & Processed) side-by-side
        """
        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setSpacing(10)

        # 1) Sidebar (QStackedWidget)
        self.setupSidebarStack()
        self.main_content_layout.addWidget(self.sidebar_stacked)

        # 2) Group Boxes
        self.setupImageGroupBoxes()
        self.main_content_layout.addWidget(self.image_area)

    # ----------------------------------------------------------------------
    # Sidebar with QStackedWidget
    # ----------------------------------------------------------------------
    def setupSidebarStack(self):
        """
        Creates a QStackedWidget with two pages:
          Page 0 = main sidebar buttons
          Page 1 = noise controls + "Back" button
        """
        # The stacked widget
        self.sidebar_stacked = QtWidgets.QStackedWidget()
        self.sidebar_stacked.setMinimumWidth(250)  # Adjust as needed
        # You could also set a minimum height if desired

        # PAGE 0: Main Buttons
        self.page_main_buttons = QtWidgets.QWidget()
        self.page_main_buttons_layout = QtWidgets.QVBoxLayout(self.page_main_buttons)
        self.page_main_buttons_layout.setSpacing(25)

        self.setupMainButtons()  # Creates the main buttons
        # Add them to the page_main_buttons_layout
        for btn in self.MAIN_BUTTONS:
            self.page_main_buttons_layout.addWidget(btn)

        self.sidebar_stacked.addWidget(self.page_main_buttons)

        # PAGE 1: Harris Operator Controls
        self.harris_operator_controls = QtWidgets.QWidget()
        self.harris_operator_layout = QtWidgets.QVBoxLayout(self.harris_operator_controls)
        self.harris_operator_layout.setSpacing(10)

        # Add noise widgets to harris_operator_layout
        self.setupHarrisWidgets()
        self.sidebar_stacked.addWidget(self.harris_operator_controls)

        # PAGE 2: SIFT Controls
        self.page_sift_controls = QtWidgets.QWidget()
        self.page_sift_layout = QtWidgets.QVBoxLayout(self.page_sift_controls)
        self.page_sift_layout.setSpacing(10)

        # Add noise widgets to harris_operator_layout
        self.setupSIFTWidgets()
        self.sidebar_stacked.addWidget(self.page_sift_controls)

        # PAGE 2: SIFT Controls
        self.page_template_matching_controls = QtWidgets.QWidget()
        self.template_matching_layout = QtWidgets.QVBoxLayout(self.page_template_matching_controls)
        self.template_matching_layout.setSpacing(10)

        # Add noise widgets to harris_operator_layout
        self.setupTemplateMatchinWidgets()
        self.sidebar_stacked.addWidget(self.page_template_matching_controls)

        # By default, show page 0
        self.sidebar_stacked.setCurrentIndex(0)

    def setupMainButtons(self):
        """
        Creates the main sidebar buttons list (Noise, Filters, etc.),
        plus sets up references so we can hide them if we want.
        """
        self.show_harris_options_button = self.util.createButton(
            "Harris Operator", self.button_style, self.show_harris_controls
        )
        self.show_sift_options_button = self.util.createButton("SIFT", self.button_style, self.show_sift_controls)
        self.show_template_matching_button = self.util.createButton("Template Matching", self.button_style, self.show_template_matching_controls)
        # We'll store these main buttons in a list if you need to show/hide them
        self.MAIN_BUTTONS = [
            self.show_harris_options_button,
            self.show_sift_options_button,
            self.show_template_matching_button
        ]
        self.kernel_sizes_array = [3, 5, 7]
        self.current_kernal_size = 3

    def setupHarrisWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in harris_operator_layout.
        """

        # Back button used on the Noise page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.harris_operator_layout.addWidget(back_button)

        # Uniform Noise
        harris_operator_label = self.util.createLabel("Harris Operator", "Color:white;", isVisible=True, isHead=True)
        self.harris_operator_layout.addWidget(harris_operator_label)

        kernal_size_label = self.util.createLabel("Kernal Size", isHead=True)
        self.harris_operator_layout.addWidget(kernal_size_label)
        self.harris_kernel_size_button = self.util.createButton(f"{self.current_kernal_size}×{self.current_kernal_size}", self.button_style, lambda: self.toggle_kernel_size(self.harris_kernel_size_button))
        self.harris_operator_layout.addWidget(self.harris_kernel_size_button)

        harris_threshold_label = self.util.createLabel("Threshold", "Color:white;", isVisible=True)
        self.harris_operator_layout.addWidget(harris_threshold_label)

        (self.harris_threshold_slider,
         harris_slider_label,
         harris_slider_layout) = self.util.createSlider(unit="%", style=self.slider_style, isVisible=True)
        self.harris_operator_layout.addLayout(harris_slider_layout)
        self.harris_operator_apply_button = self.util.createButton("Apply", self.button_style)
        self.harris_operator_layout.addWidget(self.harris_operator_apply_button)

        self.lambda_harris_operator_apply_button = self.util.createButton("Lambda Apply", self.button_style)
        self.harris_operator_layout.addWidget(self.lambda_harris_operator_apply_button)

        label01 = self.util.createLabel("", isHead=True)
        self.harris_operator_layout.addWidget(label01)

    def setupSIFTWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in harris_operator_layout.
        """
        # Back button used on the Filter page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_sift_layout.addWidget(back_button)

        self.upload_sift_photo_button = self.util.createButton("Upload Second Photo", self.button_style)
        self.page_sift_layout.addWidget(self.upload_sift_photo_button)

        sift_title = self.util.createLabel("SIFT", "color:white;", isVisible=True, isHead=True)
        self.page_sift_layout.addWidget(sift_title)

        sift_sigma_label = self.util.createLabel("Sigma - σ", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_sigma_label)
        (self.sift_sigma_slider,
         sift_sigma_slider_label,
         sift_sigma_slider_layout) = self.util.createSlider(1, 2, 1.5, "", self.slider_style, isVisible=True, is_float=True)
        self.page_sift_layout.addLayout(sift_sigma_slider_layout)

        sift_k_label = self.util.createLabel("K", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_k_label)
        (self.sift_k_spinbox,
         sift_k_slider_label,
         sift_k_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_sift_layout.addLayout(sift_k_slider_layout)

        sift_contrast_threshold_label = self.util.createLabel("Constant Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_contrast_threshold_label)
        (self.sift_contrast_threshold_spinbox,
         sift_contrast_threshold_slider_label,
         sift_contrast_threshold_slider_layout) = self.util.createSpinBox(0.01, 0.1, 0.055, is_float=True)
        self.page_sift_layout.addLayout(sift_contrast_threshold_slider_layout)

        sift_edge_threshold_label = self.util.createLabel("Edge Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_edge_threshold_label)
        (self.sift_edge_threshold_spinbox,
         sift_edge_threshold_slider_label,
         sift_edge_threshold_slider_layout) = self.util.createSpinBox(5, 20, 1, is_float=False)
        self.page_sift_layout.addLayout(sift_edge_threshold_slider_layout)

        # sift_magnitude_threshold_label = self.util.createLabel("Magnitude Threshold", "Color:white;", isVisible=True)
        # self.page_sift_layout.addWidget(sift_magnitude_threshold_label)
        # (self.sift_magnitude_threshold_spinbox,
        #  sift_magnitude_threshold_slider_label,
        #  sift_magnitude_threshold_slider_layout) = self.util.createSpinBox(1, 10, 1)
        # self.page_sift_layout.addLayout(sift_magnitude_threshold_slider_layout)

        self.sift_extract_points_button = self.util.createButton("Extract Points", self.button_style)
        self.page_sift_layout.addWidget(self.sift_extract_points_button)

        sift_normalized_label = self.util.createLabel("Normalized Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_normalized_label)

        (self.sift_normalized_threshold_slider,
         sift_normalized_threshold_slider_label,
         sift_normalized_threshold_slider_layout) = self.util.createSlider(0, 1, 0.5, is_float=True)
        self.page_sift_layout.addLayout(sift_normalized_threshold_slider_layout)

        self.sift_normalized_match_button = self.util.createButton("Normalized Match", self.button_style)
        self.page_sift_layout.addWidget(self.sift_normalized_match_button)

        sift_ssd_label = self.util.createLabel("SST Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_ssd_label)

        (self.sift_ssd_threshold_slider,
         sift_ssd_threshold_slider_label,
         sift_ssd_threshold_slider_layout) = self.util.createSlider(0, 300, 150)
        self.page_sift_layout.addLayout(sift_ssd_threshold_slider_layout)

        self.sift_ssd_match_button = self.util.createButton("SSD Match", self.button_style)
        self.page_sift_layout.addWidget(self.sift_ssd_match_button)

    def setupTemplateMatchinWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in harris_operator_layout.
        """
        # Back button used on the Filter page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.template_matching_layout.addWidget(back_button)

        self.upload_template_matching_photo_button = self.util.createButton("Upload Second Photo", self.button_style)
        self.template_matching_layout.addWidget(self.upload_template_matching_photo_button)

        self.apply_ssd_template_match_button = self.util.createButton("SSD Apply", self.button_style)
        self.template_matching_layout.addWidget(self.apply_ssd_template_match_button)

        self.apply_ncc_template_match_button = self.util.createButton("NCC Apply", self.button_style)
        self.template_matching_layout.addWidget(self.apply_ncc_template_match_button)

    def toggle_kernel_size(self, kernal_button):
        """
        Cycles through predefined kernal sizes and updates the button text to reflect the current selection.
        """
        # Get the current size from the button text
        current_size = int(kernal_button.text().split('×')[0])

        # Find the index of the current size in the kernal sizes array
        current_index = self.kernel_sizes_array.index(current_size)

        # Compute the next index; wrap around to the beginning if necessary
        next_index = (current_index + 1) % len(self.kernel_sizes_array)
        self.current_kernal_size = self.kernel_sizes_array[next_index]

        # Update the button text to the next kernal size
        kernal_button.setText(f"{self.current_kernal_size}×{self.current_kernal_size}")

    def setupImageGroupBoxes(self):
        """Creates two group boxes: Original Image & Processed Image."""
        # Calculate sizes based on screen dimensions
        default_width = int(self.screen_size.width() * (502 / 1280))
        default_height = int(self.screen_size.height() * (526 / 800))

        # Create the group boxes with default sizes
        self.original_groupBox, _ = self.util.createGroupBox(
            title="Original Image",
            size=QtCore.QSize(default_width, default_height),
            style=self.groupbox_style,
            isGraph=False
        )

        self.processed_groupBox, _ = self.util.createGroupBox(
            title="Processed Image",
            size=QtCore.QSize(default_width, default_height),
            style=self.groupbox_style,
            isGraph=False
        )

        self.additional_groupBox, _ = self.util.createGroupBox(
            title="Additional Image",
            size=QtCore.QSize(default_width, default_height),
            style=self.groupbox_style,
            isGraph=False
        )

        # Create container widgets for each layout
        self.default_container = QtWidgets.QWidget()
        self.sift_container = QtWidgets.QWidget()

        # Default layout (side by side)
        self.default_layout = QtWidgets.QHBoxLayout(self.default_container)
        self.default_layout.addWidget(self.original_groupBox)
        self.default_layout.addWidget(self.processed_groupBox)
        self.default_layout.setSpacing(10)

        # Hide the SIFT container initially
        self.sift_container.hide()
        # Hide additional group box initially
        self.additional_groupBox.hide()

        # SIFT layout will be set up when needed in show_sift_controls

        # Main image area layout
        self.image_area = QtWidgets.QWidget()
        self.main_image_layout = QtWidgets.QStackedLayout(self.image_area)
        self.main_image_layout.addWidget(self.default_container)
        self.main_image_layout.addWidget(self.sift_container)
        self.main_image_layout.setCurrentIndex(0)  # Show default layout initially

    # ----------------------------------------------------------------------
    # Retranslate
    # ----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    # ----------------------------------------------------------------------
    #  Show/Hide Logic
    # ----------------------------------------------------------------------
    def show_main_buttons(self):
        """Switch back to default layout."""
        # Reset to default sizes if we have them stored
        if hasattr(self, 'original_sizes'):
            self.processed_groupBox.setFixedSize(self.original_sizes['processed'])
            self.original_groupBox.setFixedSize(self.original_sizes['original'])
            self.additional_groupBox.setFixedSize(self.original_sizes['additional'])

        # We need to reparent the widgets back to default container
        self.original_groupBox.setParent(None)
        self.processed_groupBox.setParent(None)
        self.additional_groupBox.setParent(None)

        # Clear default layout and re-add widgets
        while self.default_layout.count():
            item = self.default_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.default_layout.addWidget(self.original_groupBox)
        self.default_layout.addWidget(self.processed_groupBox)

        # Hide additional group box
        self.additional_groupBox.hide()

        # Switch to default layout using the stacked layout
        self.main_image_layout.setCurrentIndex(0)

        # Switch to the main buttons page
        self.sidebar_stacked.setCurrentIndex(0)

    def show_harris_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(1)

    def show_sift_controls(self):
        """Switch to SIFT mode with new layout."""
        # Store original sizes
        self.original_sizes = {
            'processed': self.processed_groupBox.size(),
            'original': self.original_groupBox.size(),
            'additional': self.additional_groupBox.size()
        }

        # Calculate SIFT mode sizes
        processed_width = int(self.screen_size.width() * 0.75)
        processed_height = int(self.screen_size.height() * 0.5)
        small_width = int(processed_width * 0.48)
        small_height = int(self.screen_size.height() * 0.3)

        # Resize for SIFT mode
        self.processed_groupBox.setFixedSize(processed_width, processed_height)
        self.original_groupBox.setFixedSize(small_width, small_height)
        self.additional_groupBox.setFixedSize(small_width, small_height)

        # Set up SIFT layout - do this every time to ensure proper widget parenting
        # Clear any existing layout in the sift container
        if self.sift_container.layout():
            old_layout = self.sift_container.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            QtWidgets.QWidget().setLayout(old_layout)  # This will delete the old layout

        self.sift_layout = QtWidgets.QVBoxLayout(self.sift_container)
        self.bottom_layout = QtWidgets.QHBoxLayout()

        # We need to reparent the widgets from default container
        self.original_groupBox.setParent(None)
        self.processed_groupBox.setParent(None)
        self.additional_groupBox.setParent(None)

        self.bottom_layout.addWidget(self.original_groupBox)
        self.bottom_layout.addWidget(self.additional_groupBox)
        self.sift_layout.addWidget(self.processed_groupBox)
        self.sift_layout.addLayout(self.bottom_layout)

        # Show additional group box
        self.additional_groupBox.show()

        # Switch to SIFT layout using the stacked layout
        self.main_image_layout.setCurrentIndex(1)

        # Switch to SIFT controls page
        self.sidebar_stacked.setCurrentIndex(2)

    def show_template_matching_controls(self):
        """Switch to SIFT mode with new layout."""
        # Store original sizes
        self.original_sizes = {
            'processed': self.processed_groupBox.size(),
            'original': self.original_groupBox.size(),
            'additional': self.additional_groupBox.size()
        }

        # Calculate SIFT mode sizes
        processed_width = int(self.screen_size.width() * 0.75)
        processed_height = int(self.screen_size.height() * 0.5)
        small_width = int(processed_width * 0.48)
        small_height = int(self.screen_size.height() * 0.3)

        # Resize for SIFT mode
        self.processed_groupBox.setFixedSize(processed_width, processed_height)
        self.original_groupBox.setFixedSize(small_width, small_height)
        self.additional_groupBox.setFixedSize(small_width, small_height)

        # Set up SIFT layout - do this every time to ensure proper widget parenting
        # Clear any existing layout in the sift container
        if self.sift_container.layout():
            old_layout = self.sift_container.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            QtWidgets.QWidget().setLayout(old_layout)  # This will delete the old layout

        self.sift_layout = QtWidgets.QVBoxLayout(self.sift_container)
        self.bottom_layout = QtWidgets.QHBoxLayout()

        # We need to reparent the widgets from default container
        self.original_groupBox.setParent(None)
        self.processed_groupBox.setParent(None)
        self.additional_groupBox.setParent(None)

        self.bottom_layout.addWidget(self.original_groupBox)
        self.bottom_layout.addWidget(self.additional_groupBox)
        self.sift_layout.addWidget(self.processed_groupBox)
        self.sift_layout.addLayout(self.bottom_layout)

        # Show additional group box
        self.additional_groupBox.show()

        # Switch to SIFT layout using the stacked layout
        self.main_image_layout.setCurrentIndex(1)

        # Switch to SIFT controls page
        self.sidebar_stacked.setCurrentIndex(3)

    def toggle_matching_techniques(self):
        text = "Cross Validation" if self.toggle_matching_techniques_button.text() == "SSD" else "SSD"
        self.toggle_matching_techniques_button.setText(text)
