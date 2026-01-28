#!/usr/bin/python


import sys


from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QToolTip,
    QApplication,
    QMainWindow,
    QTabWidget,
    QStyleFactory,
)
from PyQt6.QtGui import QFont, QPalette, QColor

from numbers import Numbers
from names import Names
from lists import Lists
from teams import Teams


class StudentPicker(QMainWindow):
    """Overall class for the StudentPicker app."""

    def __init__(self):
        """Initialize the app."""

        super(StudentPicker, self).__init__()

        # Define Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e0dbcd;
            }
            QWidget {
                color: #5c5751;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 13px;
                border: none;
            }
            QTabWidget {
                background: #e0dbcd;
                border: none;
                margin: 100px;
                padding: 0px;
            }

            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabWidget::pane {
                background-color: #f5f0e6;
                border-radius: 12px;
                margin: 0px 5px 5px 5px; /* Join with tab bar */
                position: absolute;

            }
            QTabBar {
                background: #e0dbcd;
                qproperty-drawBase: 0;
                margin: 0px;

            }
            QTabBar::tab {
                background-color: #d1ccbc;
                color: #7a7469;
                padding: 10px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 2px;
                margin-top: 5px;
                font-weight: bold;

            }
            QTabBar::tab:selected {
                background-color: #f5f0e6;
                color: #5c5751;
            }
            QGroupBox {
                background-color: #edeadf;
                border-radius: 12px;
                margin-top: 20px;
                padding-top: 15px;
                font-weight: bold;
                color: #8c7d6b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #edeadf;
                color: #5c5751;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e3dec9;
            }
            QPushButton#btn_pick, QPushButton#btn_restart {
                background-color: #d97757;
                color: #ffffff;
                font-size: 15px;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton#btn_pick:hover, QPushButton#btn_restart:hover {
                background-color: #c46243;
            }
            QPushButton#btn_pick:disabled, QPushButton#btn_restart:disabled {
                background-color: #edeadf;
                color: #b0aba1;
            }
            QLineEdit, QPlainTextEdit, QSpinBox, QComboBox {
                background-color: #ffffff;
                border: 1px solid #e0dbcd;
                border-radius: 8px;
                padding: 8px;
                color: #4a4641;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #d97757;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #d97757;
                width: 0;
                height: 0;
            }
            QListView {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 5px;
                outline: 0;
                show-decoration-selected: 0;
            }
            QListView::item {
                padding: 6px 10px; /* Reduced vertical padding for density */
                border-radius: 6px;
                margin-bottom: 2px;
                color: #5c5751;
            }
            QListView::item:selected {
                background-color: #f5f0e6;
                color: #d97757;
                font-weight: bold;
                border: none;
                outline: 0;
            }
            QListView::item:selected:focus {
                background-color: #f5f0e6;
                color: #d97757;
                border: none;
                outline: 0;
            }
            QListView::item:selected:active {
                background-color: #f5f0e6;
                color: #d97757;
                border: none;
                outline: 0;
            }
            QScrollBar:vertical {
                border: none;
                background: #edeadf;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #d97757;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #c46243;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QLabel#picked_student_label {
                color: #d97757;
                font-weight: 800;
                font-size: 48px;
                background-color: transparent;
                margin: 10px;
                qproperty-alignment: 'AlignCenter';
            }
            QLabel#guide_text {
                color: #8c867a;
                font-style: italic;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background: transparent;
            }
        """)

        QApplication.setStyle(QStyleFactory.create("Fusion"))

        self.setWindowTitle("Student Picker")
        self.resize(QSize(450, 600))
        self.setMinimumSize(QSize(400, 550))
        self.move(300, 200)

        # Create tabs for the main window.
        tab_widget = QTabWidget()
        page_3 = Numbers(self)
        page_4 = Teams(self)
        page_2 = Names(self)
        page_1 = Lists(self)
        tab_widget.addTab(page_1, "Lists")
        tab_widget.addTab(page_2, "Names")
        tab_widget.addTab(page_3, "Numbers")
        tab_widget.addTab(page_4, "Teams")

        # Set the central widget of the window.
        self.setCentralWidget(tab_widget)

        self.show()


def main():

    app = QApplication(sys.argv)

    studentpicker = StudentPicker()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
