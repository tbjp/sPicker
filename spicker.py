#!/usr/bin/python


import sys, random


from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QToolTip,
    QPushButton,
    QApplication,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QLabel,
)
from PyQt6.QtGui import QFont, QPalette, QColor


class StudentPicker(QMainWindow):
    def __init__(self):
        super(StudentPicker, self).__init__()

        self.initUI()

    def initUI(self):
        """Init the app's UI."""

        self.setWindowTitle("Student Picker")
        self.resize(QSize(400, 500))
        self.setMinimumSize(QSize(400, 500))
        self.move(300, 300)

       

        topLeftLayout = QVBoxLayout()
        guideText = QLabel(
            "Enter the number of students and click "
            "the button to pick a random student.",
            wordWrap=1,
            margin=10,
        )
        topLeftLayout.addWidget(guideText)
        topLeftLayout.setContentsMargins(10, 10, 10, 10)
        self.spinBox = QSpinBox()
        self.spinBox.setValue(20)
        self.spinBox.setMinimum(1)
        self.results = []
        self.resultsString = ''
        spinBoxBox = QVBoxLayout()
        spinBoxBox.addWidget(self.spinBox)
        spinBoxBox.setContentsMargins(90, 10, 90, 90)
        topLeftLayout.addLayout(spinBoxBox)

        topRightLayout = QVBoxLayout()
        self.resultsBlock = QLabel("No results.", wordWrap=1)
        topRightLayout.addWidget(self.resultsBlock)
        self.resultsBlock.setMaximumWidth(100)

        self.createButtons()

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.button_pick)


        mainLayout = QGridLayout()
        mainLayout.addLayout(topLeftLayout, 0, 0)
        mainLayout.addLayout(topRightLayout, 0, 1)
        mainLayout.addLayout(bottomLayout, 1, 0)

        widget = QWidget()
        widget.setLayout(mainLayout)

        # Set the central widget of the window.
        self.setCentralWidget(widget)

        self.show()

    def createButtons(self):
        """Create buttons for the main window."""
        self.button_is_checked = True

        self.button_pick = QPushButton("Pick a Student", maximumWidth=100)
        self.button_pick.clicked.connect(self.button_clicked)

    def button_clicked(self):
        boxValue = self.spinBox.value()
        randomValue = random.randint(1, boxValue)
        print(randomValue)
        self.results.append(randomValue)
        self.resultsString = " ".join(list(map(str, self.results)))
        self.resultsBlock.setText(self.resultsString)


class ColorBlock(QWidget):
    def __init__(self, color):
        super(ColorBlock, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


def main():

    app = QApplication(sys.argv)

    studentpicker = StudentPicker()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
