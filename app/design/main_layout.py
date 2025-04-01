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

        self.original_groupBox.show()
        self.processed_groupBox.show()

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

        self.quit_app_button = self.util.createButton("X", self.quit_button_style)
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
        images_layout = QtWidgets.QHBoxLayout()
        images_layout.setSpacing(10)
        images_layout.addWidget(self.original_groupBox)
        images_layout.addWidget(self.processed_groupBox)

        self.main_content_layout.addLayout(images_layout)

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

        # PAGE 3: Mathcing Controls
        self.page_matching_controls = QtWidgets.QWidget()
        self.page_matching_layout = QtWidgets.QVBoxLayout(self.page_matching_controls)
        self.page_matching_layout.setSpacing(10)

        self.setupMatchingWidgets()
        self.sidebar_stacked.addWidget(self.page_matching_controls)

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
        self.show_matching_options_button = self.util.createButton("Matching", self.button_style, self.show_matching_controls)

        # We'll store these main buttons in a list if you need to show/hide them
        self.MAIN_BUTTONS = [
            self.show_harris_options_button,
            self.show_sift_options_button,
            self.show_matching_options_button,
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

        label01 = self.util.createLabel("", isHead=True)
        self.harris_operator_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.harris_operator_layout.addWidget(label02)

    def setupSIFTWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in harris_operator_layout.
        """
        # Back button used on the Filter page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_sift_layout.addWidget(back_button)

        sift_title = self.util.createLabel("SIFT", "color:white;", isVisible=True, isHead=True)
        self.page_sift_layout.addWidget(sift_title)

        sift_sigma_label = self.util.createLabel("Sigma - σ", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_sigma_label)
        (self.sift_sigma_slider,
         sift_sigma_slider_label,
         sift_sigma_slider_layout) = self.util.createSlider(1, 10, 5, "", self.slider_style, isVisible=True)
        self.page_sift_layout.addLayout(sift_sigma_slider_layout)

        sift_k_label = self.util.createLabel("K", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_k_label)
        (self.sift_k_spinbox,
         sift_k_slider_label,
         sift_k_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_sift_layout.addLayout(sift_k_slider_layout)

        sift_constant_threshold_label = self.util.createLabel("Constant Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_constant_threshold_label)
        (self.sift_constant_threshold_spinbox,
         sift_constant_threshold_slider_label,
         sift_constant_threshold_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_sift_layout.addLayout(sift_constant_threshold_slider_layout)

        sift_edge_threshold_label = self.util.createLabel("Edge Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_edge_threshold_label)
        (self.sift_edge_threshold_spinbox,
         sift_edge_threshold_slider_label,
         sift_edge_threshold_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_sift_layout.addLayout(sift_edge_threshold_slider_layout)

        sift_magnitude_threshold_label = self.util.createLabel("Magnitude Threshold", "Color:white;", isVisible=True)
        self.page_sift_layout.addWidget(sift_magnitude_threshold_label)
        (self.sift_magnitude_threshold_spinbox,
         sift_magnitude_threshold_slider_label,
         sift_magnitude_threshold_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_sift_layout.addLayout(sift_magnitude_threshold_slider_layout)

        self.upload_sift_photo_button = self.util.createButton("Upload Second Photo", self.button_style)
        self.page_sift_layout.addWidget(self.upload_sift_photo_button)

        self.sift_extract_points_button = self.util.createButton("Extract Points", self.button_style)
        self.page_sift_layout.addWidget(self.sift_extract_points_button)

        self.sift_match_button = self.util.createButton("Match", self.button_style)
        self.page_sift_layout.addWidget(self.sift_match_button)

    def setupMatchingWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in harris_operator_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_matching_layout.addWidget(back_button)

        # =========================================================================================================
        matching_techniques_label = self.util.createLabel("Matching Techs", isHead=True)
        self.page_matching_layout.addWidget(matching_techniques_label)

        self.toggle_matching_techniques_button = self.util.createButton("SSD", self.button_style, self.toggle_matching_techniques)
        self.page_matching_layout.addWidget(self.toggle_matching_techniques_button)

        self.upload_matching_photo_button = self.util.createButton("Upload Second Photo", self.button_style)
        self.page_matching_layout.addWidget(self.upload_matching_photo_button)

        self.match_photos_button = self.util.createButton("Match", self.button_style)
        self.page_matching_layout.addWidget(self.match_photos_button)

        label01 = self.util.createLabel("", isHead=True)
        self.page_matching_layout.addWidget(label01)

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
        self.original_groupBox, _ = self.util.createGroupBox(
            title="Original Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)), int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )
        self.processed_groupBox, _ = self.util.createGroupBox(
            title="Processed Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)), int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )
        self.additional_groupBox, _ = self.util.createGroupBox(
            title="Additional Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)), int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )

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
        """
        Switches back to the main buttons page, shows the original and processed group boxes,
        and hides the hybrid image group boxes.
        """
        # Show the original and processed group boxes
        self.original_groupBox.show()
        self.processed_groupBox.show()

        # Switch to the main buttons page
        self.sidebar_stacked.setCurrentIndex(0)  # Assuming main buttons page is at index 0

    def show_harris_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(1)

    def show_sift_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(2)

    def show_matching_controls(self):
        self.sidebar_stacked.setCurrentIndex(3)

    def toggle_matching_techniques(self):
        text = "Cross Validation" if self.toggle_matching_techniques_button.text() == "SSD" else "SSD"
        self.toggle_matching_techniques_button.setText(text)
