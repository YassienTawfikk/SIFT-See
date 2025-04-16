from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from PyQt5 import QtWidgets

MAIN_COLOR = "rgb(30, 0, 0)"
SECONDARY_COLOR = "rgb(30, 10, 10)"
BUTTON_STYLE = F"""
    QPushButton {{
        background-color: black;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        border: 1px solid white;
    }}
    QPushButton:hover {{
        background-color: {SECONDARY_COLOR};
    }}
"""
QUIT_BUTTON_STYLE = f"""
    QPushButton {{
        color: white;
        border: 3px solid white;
    }}
    QPushButton:hover {{
        border-color: rgb(253, 94, 80);
        color: rgb(253, 94, 80);
    }}
"""
GROUPBOX_STYLE = f"""
    color: white;
    border: 1px solid white;
"""
SLIDER_STYLE = f"""
QSlider::groove:horizontal {{
    border: 1px solid #999999;
    height: 2px;
    background: rgb(60, 0, 0);
    margin: 2px 0;
}}
QSlider::handle:horizontal {{
    background: black;
    width: 16px;
    margin: -10px 0;
    border-radius: 3px;
    border: 1px solid white;
}}
QSlider::sub-page:horizontal {{
    background: white;
    border: 1px solid {SECONDARY_COLOR};
    height: 2px;
    border-radius: 2px;
}}
"""
SPINBOX_STYLE = f"""
"""


class GUIUtilities:
    def __init__(self):
        pass  # Initialize any instance variables if necessary

    def adjust_quit_button(self, button):
        button.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Hiragino Sans GB")
        font.setPointSize(40)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(False)
        button.setFont(font)
        button.setStyleSheet(QUIT_BUTTON_STYLE)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setLayoutDirection(QtCore.Qt.LeftToRight)
        button.setMinimumSize(50, 50)
        button.setMaximumSize(50, 50)

    def createButton(self, text, style=BUTTON_STYLE, method=False, isVisible=True):
        button = QtWidgets.QPushButton()
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(style)
        button.setText(text)
        button.setMinimumSize(200, 50)
        button.setMaximumSize(200, 50)
        if not isVisible:
            button.hide()
        if method:
            button.clicked.connect(method)
        return button

    def createGroupBox(self, title, size, style=GROUPBOX_STYLE, isGraph=False):
        groupBox = QtWidgets.QGroupBox()
        groupBox.setTitle(title)
        groupBox.setMinimumSize(size)
        groupBox.setMaximumSize(size)
        groupBox.setStyleSheet(style)
        widget = None

        if isGraph:
            widget = self.addGraphView(groupBox)
        else:
            # Create a QLabel to display HRV data
            label = QtWidgets.QLabel(groupBox)
            label.setStyleSheet("color: white; background-color: transparent; border: none;")
            label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            label.setFixedSize(600, 250)  # Adjust width and height as needed

            # Add label to the group box layout
            group_box_layout = QtWidgets.QVBoxLayout(groupBox)
            group_box_layout.setContentsMargins(10, 10, 10, 10)
            group_box_layout.addWidget(label)

            widget = label  # Assign label to the widget variable

        return groupBox, widget

    def addGraphView(self, group_box):
        """ Creates a Pyqtgraph plot widget for real-time data visualization. """
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground('w')
        plot_widget.showGrid(x=True, y=True)

        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(plot_widget)
        graph_layout.setContentsMargins(5, 25, 5, 5)

        group_box.setLayout(graph_layout)
        return plot_widget

    def createSlider(self, min_value=0, max_value=100, initial_value=50, unit=None, style=SLIDER_STYLE, isVisible=True):
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(10)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(initial_value)
        slider.setMaximumSize(180, 50)

        unit_text = unit if unit is not None else ""
        label = QtWidgets.QLabel(f"{initial_value}{unit_text}")
        label.setMinimumWidth(25)
        label.setMaximumHeight(50)
        label.setStyleSheet("color:white;")

        def update_label(value):
            label.setText(f"{value}{unit_text}")

        slider.valueChanged.connect(update_label)
        if style:
            slider.setStyleSheet(style)
        if not isVisible:
            slider.hide()
            label.hide()

        slider_layout.addWidget(slider)
        slider_layout.addWidget(label)

        return slider, label, slider_layout

    def createSpinBox(self, min_value=0, max_value=100, initial_value=50, unit=None, style=SPINBOX_STYLE, isVisible=True, is_float=False):
        spinbox_layout = QtWidgets.QHBoxLayout()
        spinbox_layout.setContentsMargins(0, 0, 0, 0)
        spinbox_layout.setSpacing(10)

        # Use QDoubleSpinBox if float is required
        spinbox = QtWidgets.QDoubleSpinBox() if is_float else QtWidgets.QSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(initial_value)
        spinbox.setMinimumWidth(180)
        spinbox.setMaximumWidth(180)

        if is_float:
            spinbox.setDecimals(2)  # Optional: specify number of decimals
            spinbox.setSingleStep(0.1)

        unit_text = unit if unit is not None else ""
        label = QtWidgets.QLabel(f"{initial_value}{unit_text}")
        label.setMinimumWidth(30)
        label.setStyleSheet("color: white;")

        def update_label(value):
            label.setText(f"{value:.2f}{unit_text}" if is_float else f"{int(value)}{unit_text}")

        spinbox.valueChanged.connect(update_label)
        spinbox.setStyleSheet(style if style else "color:white")

        if not isVisible:
            spinbox.hide()
            label.hide()

        spinbox_layout.addWidget(spinbox)
        spinbox_layout.addWidget(label)

        return spinbox, label, spinbox_layout

    def createLabel(self, text, style=None, isVisible=True, isHead=False):
        label = QtWidgets.QLabel()
        label.setText(text)

        font = QtGui.QFont()
        if isHead:
            font.setPointSize(24)
            current_height = 80
            font.setBold(True)
            font.setItalic(False)
        else:
            font.setPointSize(16)
            current_height = 20
            font.setBold(False)
            font.setItalic(True)
        label.setFont(font)
        label.setMaximumHeight(current_height)

        if style:
            label.setStyleSheet(style)
        else:
            label.setStyleSheet("color: white;")

        if not isVisible:
            label.hide()

        return label
