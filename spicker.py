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


class StudentPicker(QMainWindow):
    """Overall class for the StudentPicker app."""

    def __init__(self):
        """Initialize the app."""

        super(StudentPicker, self).__init__()

        # Define Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #faf7f2;
            }
            QWidget {
                background-color: #faf7f2;
                color: #5c5751;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 13px;
                border: none;
            }
            QTabWidget::pane {
                background-color: #f5f0e6;
                border-radius: 12px;
                margin: 5px;
            }
            QTabBar::tab {
                background-color: #edeadf;
                color: #8c867a;
                padding: 12px 24px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 4px;
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
            QListView {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 5px;
            }
            QListView::item {
                padding: 8px;
                border-radius: 4px;
                margin-bottom: 2px;
            }
            QListView::item:selected {
                background-color: #f5f0e6;
                color: #d97757;
                font-weight: bold;
            }
            QLabel#picked_student_label {
                color: #d97757;
                font-weight: 800;
                font-size: 48px;
                background-color: transparent;
                margin: 10px;
            }
            QLabel#guide_text {
                color: #8c867a;
                font-style: italic;
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
        page_2 = Names(self)
        page_1 = Lists(self)
        tab_widget.addTab(page_1, "Lists")
        tab_widget.addTab(page_2, "Names")
        tab_widget.addTab(page_3, "Numbers")

        # Set the central widget of the window.
        self.setCentralWidget(tab_widget)

        self.show()


def main():

    app = QApplication(sys.argv)

    studentpicker = StudentPicker()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
