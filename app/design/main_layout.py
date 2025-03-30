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
        self.main_window_style = "background-color: #040d12;"
        self.button_style = """
            QPushButton {
                background-color: rgb(30, 30, 30);
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
                border: 1px solid white;
            }
            QPushButton:hover {
                background-color: rgb(40, 40, 40);
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
                background: #dddddd;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: rgb(11, 62, 159);
                width: 16px;
                margin: -10px 0;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: rgb(4, 29, 127);
                border: 1px solid rgb(4, 29, 127);
                height: 1px;
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
            text="Pixelizing",
            style="color:white; padding:10px; padding-left:0;",
            isHead=True
        )
        font = QtGui.QFont()
        font.setPointSize(30)
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

        # PAGE 1: Noise Controls
        self.page_noise_controls = QtWidgets.QWidget()
        self.page_noise_layout = QtWidgets.QVBoxLayout(self.page_noise_controls)
        self.page_noise_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupNoiseWidgets()
        self.sidebar_stacked.addWidget(self.page_noise_controls)

        # PAGE 2: Filter Controls
        self.page_filter_controls = QtWidgets.QWidget()
        self.page_filter_layout = QtWidgets.QVBoxLayout(self.page_filter_controls)
        self.page_filter_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupFilterWidgets()
        self.sidebar_stacked.addWidget(self.page_filter_controls)

        # PAGE 3: Edge Detection Controls
        self.page_edge_detection_controls = QtWidgets.QWidget()
        self.page_edge_detection_layout = QtWidgets.QVBoxLayout(self.page_edge_detection_controls)
        self.page_edge_detection_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupEdgeDetectionWidgets()
        self.sidebar_stacked.addWidget(self.page_edge_detection_controls)

        # PAGE 4: Refine Image Controls
        self.page_refine_image_controls = QtWidgets.QWidget()
        self.page_refine_image_layout = QtWidgets.QVBoxLayout(self.page_refine_image_controls)
        self.page_refine_image_layout.setSpacing(10)

        self.setupRefineImageWidgets()
        self.sidebar_stacked.addWidget(self.page_refine_image_controls)

        # PAGE 5: Fourier Filter Controls
        self.page_fourier_filter_controls = QtWidgets.QWidget()
        self.page_fourier_filter_layout = QtWidgets.QVBoxLayout(self.page_fourier_filter_controls)
        self.page_fourier_filter_layout.setSpacing(10)

        self.setupFourierFilterWidgets()
        self.sidebar_stacked.addWidget(self.page_fourier_filter_controls)

        # PAGE 6: Threshold Controls
        self.page_threshold_controls = QtWidgets.QWidget()
        self.page_threshold_layout = QtWidgets.QVBoxLayout(self.page_threshold_controls)
        self.page_threshold_layout.setSpacing(10)

        self.setupThresholdWidgets()
        self.sidebar_stacked.addWidget(self.page_threshold_controls)

        # PAGE 7: Hybrid Image Controls
        self.page_hybrid_image_controls = QtWidgets.QWidget()
        self.page_hybrid_image_layout = QtWidgets.QVBoxLayout(self.page_hybrid_image_controls)
        self.page_hybrid_image_layout.setSpacing(10)
        self.setupHybridImageWidgets()
        self.sidebar_stacked.addWidget(self.page_hybrid_image_controls)

        # By default, show page 0
        self.sidebar_stacked.setCurrentIndex(0)

    def setupMainButtons(self):
        """
        Creates the main sidebar buttons list (Noise, Filters, etc.),
        plus sets up references so we can hide them if we want.
        """
        self.show_noise_options_button = self.util.createButton(
            "Noise", self.button_style, self.show_noise_controls
        )
        self.show_filter_options_button = self.util.createButton("Filters", self.button_style, self.show_filter_controls)
        self.show_edge_detecting_options_button = self.util.createButton("Edge Detector", self.button_style, self.show_edge_detection_controls)
        self.show_metrics_button = self.util.createButton("View Metrics", self.button_style)
        self.show_refine_options_button = self.util.createButton("Refine Image", self.button_style, self.show_refine_image_controls)
        self.show_threshold_options_button = self.util.createButton("Thresholding", self.button_style, self.show_threshold_controls)
        self.grayscaling_button = self.util.createButton("Gray Scaling", self.button_style)
        self.show_fourier_filter_options_button = self.util.createButton("Fourier Filters", self.button_style, self.show_fourier_filter_controls)
        self.upload_hybrid_image_button = self.util.createButton("Hybrid Image", self.button_style, self.show_hybrid_image_controls)

        # We'll store these main buttons in a list if you need to show/hide them
        self.MAIN_BUTTONS = [
            self.show_noise_options_button,
            self.show_filter_options_button,
            self.show_edge_detecting_options_button,
            self.show_metrics_button,
            self.show_refine_options_button,
            self.show_threshold_options_button,
            self.grayscaling_button,
            self.show_fourier_filter_options_button,
            self.upload_hybrid_image_button
        ]
        self.kernel_sizes_array = [3, 5, 7]
        self.current_kernal_size = 3

    def setupNoiseWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """

        # Back button used on the Noise page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_noise_layout.addWidget(back_button)

        # Uniform Noise
        uniform_title = self.util.createLabel("Uniform Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(uniform_title)

        uniform_label = self.util.createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(uniform_label)

        (self.uniform_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSlider(unit="%", style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)
        self.uniform_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.uniform_noise_button)

        # Gaussian Noise
        gaussian_title = self.util.createLabel("Gaussian Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(gaussian_title)

        mean_label = self.util.createLabel("Mean", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(mean_label)

        (self.mean_gaussian_noise_slider,
         mean_slider_label,
         mean_slider_layout) = self.util.createSlider(min_value=-10, max_value=10, initial_value=0, style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(mean_slider_layout)

        # This second label was "Mean" in your original code
        stddev_label = self.util.createLabel("Standard Deviation", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(stddev_label)

        (self.stddev_gaussian_noise_slider,
         stddev_val_label,
         stddev_layout) = self.util.createSlider(min_value=0, max_value=100, initial_value=50, style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(stddev_layout)

        self.gaussian_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.gaussian_noise_button)

        # Salt & Pepper Noise
        salt_pepper_noise_title = self.util.createLabel("Salt & Pepper Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_title)

        salt_pepper_noise_label = self.util.createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_label)

        (self.salt_pepper_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSlider(unit="%", style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)
        self.salt_pepper_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.salt_pepper_noise_button)

    def setupFilterWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        # Back button used on the Filter page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_filter_layout.addWidget(back_button)

        kernal_size_label = self.util.createLabel("Kernal Size", isHead=True)
        self.page_filter_layout.addWidget(kernal_size_label)
        self.filter_kernel_size_button = self.util.createButton(f"{self.current_kernal_size}×{self.current_kernal_size}", self.button_style, lambda: self.toggle_kernel_size(self.filter_kernel_size_button))
        self.page_filter_layout.addWidget(self.filter_kernel_size_button)

        average_filter_title = self.util.createLabel("Average Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(average_filter_title)
        self.average_filter_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.average_filter_button)

        gaussian_filter_title = self.util.createLabel("Gaussian Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(gaussian_filter_title)
        gaussian_filter_sigma_label = self.util.createLabel("Sigma - σ", "Color:white;", isVisible=True)
        self.page_filter_layout.addWidget(gaussian_filter_sigma_label)
        (self.gaussian_filter_sigma_spinbox,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSpinBox(1, 10, 1)
        self.page_filter_layout.addLayout(uniform_slider_layout)
        self.gaussian_filter_apply_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.gaussian_filter_apply_button)

        median_filter_title = self.util.createLabel("Median Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(median_filter_title)
        self.median_filter_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.median_filter_button)

    def setupEdgeDetectionWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_edge_detection_layout.addWidget(back_button)

        # =========================================================================================================
        sobel_label = self.util.createLabel("Sobel Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(sobel_label)
        self.sobel_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.sobel_edge_detection_button)

        # =========================================================================================================
        roberts_label = self.util.createLabel("Roberts Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(roberts_label)
        self.roberts_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.roberts_edge_detection_button)

        # =========================================================================================================
        canny_label = self.util.createLabel("Canny Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(canny_label)

        high_threshold_label = self.util.createLabel("High Threshold")
        self.page_edge_detection_layout.addWidget(high_threshold_label)

        (self.edge_detection_high_threshold_spinbox,
         edge_detection_high_threshold_label,
         edge_detection_high_threshold_layout) = self.util.createSpinBox(0, 400, 100)
        self.page_edge_detection_layout.addLayout(edge_detection_high_threshold_layout)
        self.edge_detection_high_threshold_spinbox.valueChanged.connect(self.update_low_threshold)

        low_threshold_label = self.util.createLabel("Low Threshold")
        self.page_edge_detection_layout.addWidget(low_threshold_label)

        (self.edge_detection_low_threshold_spinbox,
         edge_detection_low_threshold_label,
         edge_detection_low_threshold_layout) = self.util.createSpinBox(0, 200, 50)

        self.page_edge_detection_layout.addLayout(edge_detection_low_threshold_layout)
        self.edge_detection_low_threshold_spinbox.valueChanged.connect(self.update_high_threshold)

        self.canny_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.canny_edge_detection_button)

        # =========================================================================================================
        prewitt_label = self.util.createLabel("Prewitt Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(prewitt_label)
        self.prewitt_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.prewitt_edge_detection_button)

    def setupRefineImageWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_refine_image_layout.addWidget(back_button)

        # =========================================================================================================
        normalize_label = self.util.createLabel("Normalize", isHead=True)
        self.page_refine_image_layout.addWidget(normalize_label)
        self.normalize_image_button = self.util.createButton("Apply", self.button_style)
        self.page_refine_image_layout.addWidget(self.normalize_image_button)

        # =========================================================================================================
        equalize_label = self.util.createLabel("Equalize", isHead=True)
        self.page_refine_image_layout.addWidget(equalize_label)
        self.equalize_image_button = self.util.createButton("Apply", self.button_style)
        self.page_refine_image_layout.addWidget(self.equalize_image_button)

        # =========================================================================================================
        label01 = self.util.createLabel("", isHead=True)
        self.page_refine_image_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.page_refine_image_layout.addWidget(label02)

    def setupFourierFilterWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_fourier_filter_layout.addWidget(back_button)

        # =========================================================================================================
        hpf_label = self.util.createLabel("High Pass Filter", isHead=True)
        self.page_fourier_filter_layout.addWidget(hpf_label)
        self.hpf_button = self.util.createButton("Apply", self.button_style)
        self.page_fourier_filter_layout.addWidget(self.hpf_button)

        # =========================================================================================================
        lpf_label = self.util.createLabel("Low Pass Filter", isHead=True)
        self.page_fourier_filter_layout.addWidget(lpf_label)
        self.lpf_button = self.util.createButton("Apply", self.button_style)
        self.page_fourier_filter_layout.addWidget(self.lpf_button)

        # =========================================================================================================
        raduis_control_title = self.util.createLabel("Raduis Control", isHead=True)
        self.page_fourier_filter_layout.addWidget(raduis_control_title)
        (self.raduis_control_slider,
         raduis_control_label,
         raduis_control_layout) = self.util.createSlider(0, 50, 25, "%", self.slider_style, )
        self.page_fourier_filter_layout.addLayout(raduis_control_layout)

        # label01 = self.util.createLabel("", isHead=True)
        # self.page_fourier_filter_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.page_fourier_filter_layout.addWidget(label02)
        label03 = self.util.createLabel("", isHead=True)
        self.page_fourier_filter_layout.addWidget(label03)

    def setupThresholdWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_threshold_layout.addWidget(back_button)

        # =========================================================================================================
        local_threshold_label = self.util.createLabel("Local Threshold", isHead=True)
        self.page_threshold_layout.addWidget(local_threshold_label)

        block_size_label = self.util.createLabel("Block Size")
        self.page_threshold_layout.addWidget(block_size_label)

        (self.local_block_size_spinbox,
         local_block_size_label,
         local_block_size_layout) = self.util.createSpinBox(0, 100, 50)
        self.page_threshold_layout.addLayout(local_block_size_layout)

        self.local_threshold_button = self.util.createButton("Apply", self.button_style)
        self.page_threshold_layout.addWidget(self.local_threshold_button)

        # =========================================================================================================
        global_threshold_label = self.util.createLabel("Global Threshold", isHead=True)
        self.page_threshold_layout.addWidget(global_threshold_label)

        global_threshold_label = self.util.createLabel("Threshold")
        self.page_threshold_layout.addWidget(global_threshold_label)

        (self.global_threshold_spinbox,
         global_threshold_threshold_label,
         global_threshold_layout) = self.util.createSpinBox(0, 100, 50)
        self.page_threshold_layout.addLayout(global_threshold_layout)

        self.global_threshold_button = self.util.createButton("Apply", self.button_style)
        self.page_threshold_layout.addWidget(self.global_threshold_button)

        label01 = self.util.createLabel("", isHead=True)
        self.page_threshold_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.page_threshold_layout.addWidget(label02)
        label03 = self.util.createLabel("", isHead=True)
        self.page_threshold_layout.addWidget(label03)

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

    def setupHybridImageWidgets(self):
        """
        Sets up the layout for the hybrid image page but does not create the widgets yet.
        """
        # Back button to return to the main buttons
        self.back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_hybrid_image_layout.addWidget(self.back_button)

        # Create upload buttons for low-frequency and high-frequency images
        self.upload_low_freq_button = self.util.createButton("Upload Image 1", self.button_style)
        self.upload_high_freq_button = self.util.createButton("Upload Image 2", self.button_style)
        self.generate_hybrid_image_button = self.util.createButton("Hybrid Image", self.button_style)

        # Store the buttons as attributes of the class
        self.upload_low_freq_button.setObjectName("upload_low_freq_button")
        self.upload_high_freq_button.setObjectName("upload_high_freq_button")
        self.generate_hybrid_image_button.setObjectName("generate_hybrid_image_button")

        # Create a horizontal layout for the upload buttons
        upload_buttons_layout = QtWidgets.QHBoxLayout()
        upload_buttons_layout.addWidget(self.upload_low_freq_button)
        upload_buttons_layout.addWidget(self.upload_high_freq_button)
        upload_buttons_layout.addWidget(self.generate_hybrid_image_button)

        # Add the upload buttons layout to the page_hybrid_image_layout
        self.page_hybrid_image_layout.addLayout(upload_buttons_layout)

        # Placeholder for the group boxes (they will be created dynamically)
        self.low_frequency_groupbox = None
        self.high_frequency_groupbox = None
        self.hybrid_image_groupbox = None

    def addHybridImageWidgets(self):
        """
        Dynamically creates and adds the group boxes for low-frequency, high-frequency, and hybrid images.
        Also adds two upload buttons for low-frequency and high-frequency images.
        """
        if self.low_frequency_groupbox is None:  # Check if widgets are already created
            # Create the group boxes
            self.low_frequency_groupbox, _ = self.util.createGroupBox(
                title="Low Frequency Image",
                size=QtCore.QSize(int(self.screen_size.width() * (402 / 1280)),
                                  int(self.screen_size.height() * (426 / 800))),
                style=self.groupbox_style,
                isGraph=False
            )
            self.high_frequency_groupbox, _ = self.util.createGroupBox(
                title="High Frequency Image",
                size=QtCore.QSize(int(self.screen_size.width() * (402 / 1280)),
                                  int(self.screen_size.height() * (426 / 800))),
                style=self.groupbox_style,
                isGraph=False
            )
            self.hybrid_image_groupbox, _ = self.util.createGroupBox(
                title="Hybrid Image",
                size=QtCore.QSize(int(self.screen_size.width() * (402 / 1280)),
                                  int(self.screen_size.height() * (426 / 800))),
                style=self.groupbox_style,
                isGraph=False
            )

            # Create a horizontal layout for the group boxes
            group_boxes_layout = QtWidgets.QHBoxLayout()
            group_boxes_layout.addWidget(self.low_frequency_groupbox)
            group_boxes_layout.addWidget(self.high_frequency_groupbox)
            group_boxes_layout.addWidget(self.hybrid_image_groupbox)

            # Add the group boxes layout to the page_hybrid_image_layout
            self.page_hybrid_image_layout.addLayout(group_boxes_layout)

    def update_high_threshold(self, low_threshold_value):
        """
        Adjusts the high threshold based on changes in the low threshold to ensure it's always higher.
        """
        high_threshold_value = self.edge_detection_high_threshold_spinbox.value()
        if low_threshold_value >= high_threshold_value:
            new_high_value = low_threshold_value + 1
            self.edge_detection_high_threshold_spinbox.setValue(min(new_high_value, self.edge_detection_high_threshold_spinbox.maximum()))

    def update_low_threshold(self, high_threshold_value):
        """
        Adjusts the low threshold based on changes in the high threshold to ensure it's always lower.
        """
        low_threshold_value = self.edge_detection_low_threshold_spinbox.value()
        if high_threshold_value <= low_threshold_value:
            new_low_value = high_threshold_value - 1
            self.edge_detection_low_threshold_spinbox.setValue(max(new_low_value, self.edge_detection_low_threshold_spinbox.minimum()))

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

        # Hide the hybrid image group boxes
        if self.low_frequency_groupbox is not None:
            self.low_frequency_groupbox.hide()
        if self.high_frequency_groupbox is not None:
            self.high_frequency_groupbox.hide()
        if self.hybrid_image_groupbox is not None:
            self.hybrid_image_groupbox.hide()

        # Switch to the main buttons page
        self.sidebar_stacked.setCurrentIndex(0)  # Assuming main buttons page is at index 0

    def show_noise_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(1)

    def show_filter_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(2)

    def show_edge_detection_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(3)

    def show_refine_image_controls(self):
        self.sidebar_stacked.setCurrentIndex(4)

    def show_fourier_filter_controls(self):
        self.sidebar_stacked.setCurrentIndex(5)

    def show_threshold_controls(self):
        self.sidebar_stacked.setCurrentIndex(6)

    def show_hybrid_image_controls(self):
        """
        Switches to the hybrid image page, hides the original and processed group boxes,
        and dynamically adds the hybrid image widgets if they don't already exist.
        """
        # Hide the original and processed group boxes
        self.original_groupBox.hide()
        self.processed_groupBox.hide()

        # Switch to the hybrid image page
        self.sidebar_stacked.setCurrentIndex(7)  # Assuming hybrid image page is at index 7

        # Dynamically add the hybrid image widgets if they don't already exist
        self.addHybridImageWidgets()

        # Ensure the hybrid image group boxes are visible
        if self.low_frequency_groupbox is not None:
            self.low_frequency_groupbox.show()
        if self.high_frequency_groupbox is not None:
            self.high_frequency_groupbox.show()
        if self.hybrid_image_groupbox is not None:
            self.hybrid_image_groupbox.show()
