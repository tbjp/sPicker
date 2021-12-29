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


class StudentPicker(QMainWindow):
    """Overall class for the StudentPicker app."""

    def __init__(self):
        """Initialize the app."""

        super(StudentPicker, self).__init__()

        QApplication.setStyle(QStyleFactory.create("Fusion"))

        self.setWindowTitle("Student Picker")
        self.resize(QSize(400, 500))
        self.setMinimumSize(QSize(400, 500))
        self.move(300, 200)

        # Create tabs for the main window.
        tab_widget = QTabWidget()
        page_1 = Numbers(self)
        page_2 = Names(self)
        tab_widget.addTab(page_1, "Numbers")
        tab_widget.addTab(page_2, "Names")        

        # Set the central widget of the window.
        self.setCentralWidget(tab_widget)

        self.show()


def main():

    app = QApplication(sys.argv)

    studentpicker = StudentPicker()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
