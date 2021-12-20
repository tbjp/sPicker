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
    QGroupBox,
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

        self.create_buttons()

        # Settings
        def_ss = 3  # Default num of students
        max_ss = 50  # Max num of students

        # Fonts
        result_font = QFont()
        result_font.setPointSize(50)

        # Create default variables.
        self.ss_num_list = list(range(1, def_ss))
        self.ss_picked_list = []
        self.resultsString = ""
        self.ss_unpicked_list_label = QLabel("PH", wordWrap=100)
        self.picked_student_label = QLabel("00")
        self.picked_student_label.setFont(result_font)
        self.btn_pick_clicked_restart_flag = 0

        # Top left box - result and user settings
        topLeftLayout = QVBoxLayout()
        topLeftGroupBox1 = QGroupBox("Chosen Student")
        topLeftGroupBox1Layout = QVBoxLayout()
        topLeftGroupBox1.setLayout(topLeftGroupBox1Layout)
        topLeftGroupBox1Layout.addWidget(self.picked_student_label)

        guideText = QLabel(
            "Enter the number of students and click "
            "the button to pick a random student.",
            wordWrap=1,
            margin=10,
        )

        topLeftLayout.addWidget(topLeftGroupBox1)
        topLeftLayout.addWidget(guideText)
        topLeftLayout.setContentsMargins(10, 10, 10, 10)
        self.spinBox = QSpinBox()
        self.spinBox.setValue(def_ss)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(max_ss)
        spinBoxBox = QHBoxLayout()
        spinBoxBox.addWidget(self.spinBox)
        spinBoxBox.addWidget(self.btn_new_list)
        spinBoxBox.setContentsMargins(50, 10, 50, 10)
        topLeftLayout.addLayout(spinBoxBox)

        # Top right box - lists and results
        topRightLayout = QVBoxLayout()

        # --- Unpicked students group box
        topRightGroupBox1 = QGroupBox("Unpicked Students")
        topRightGroupBox1Layout = QVBoxLayout()
        self.ss_picked_list_label = QLabel("No results.", wordWrap=1000)
        self.btn_new_list_clicked()
        topRightGroupBox1.setLayout(topRightGroupBox1Layout)
        topRightGroupBox1Layout.addWidget(self.ss_unpicked_list_label)
        topRightLayout.addWidget(topRightGroupBox1)

        topRightGroupBox2 = QGroupBox("Picked Students")
        topRightGroupBox2Layout = QVBoxLayout()
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_label)
        topRightGroupBox2.setLayout(topRightGroupBox2Layout)
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_label)
        topRightLayout.addWidget(topRightGroupBox2)

        self.ss_unpicked_list_label.setMaximumWidth(200)
        self.ss_picked_list_label.setMaximumWidth(200)

        # Bottom box - big button
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.btn_pick)

        # Main Layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLeftLayout, 0, 0)
        mainLayout.addLayout(topRightLayout, 0, 1)
        mainLayout.addLayout(bottomLayout, 1, 0)

        widget = QWidget()
        widget.setLayout(mainLayout)

        # Set the central widget of the window.
        self.setCentralWidget(widget)

        self.show()

    def create_buttons(self):
        """Create buttons for the main window."""
        self.btn_pick = QPushButton("Pick a Student", maximumWidth=1000)
        self.btn_pick.clicked.connect(self.btn_pick_clicked)

        self.btn_new_list = QPushButton("Create", maximumWidth=100)
        self.btn_new_list.clicked.connect(self.btn_new_list_clicked)

    def btn_pick_clicked(self):
        """Pick a student from the list, show result (and remove)."""
        x = self.ss_unpicked_list
        print(x)

        rf = self.btn_pick_clicked_restart_flag

        if x:
            rf = 0  # Still students in list
            randomValue = random.choice(x)
            print(randomValue)
            self.ss_unpicked_list.remove(randomValue)
            self.ss_picked_list.append(randomValue)
            self.update_labels(randomValue)
            print(f"RF: {rf}")

        if not x and rf == 0:
            rf = 1
            print(f"RF: {rf}")

        if rf == 1:  # No students in list.
            self.ss_unpicked_list_label.setText("All students picked.")
            self.btn_pick.setText("Restart")
            rf = 2
        elif rf == 2:  # Restart button pressed.
            self.btn_new_list_clicked()
            self.btn_pick.setText("Pick a Student")
            rf = 0
            print(f"RF: {rf}")

        self.btn_pick_clicked_restart_flag = rf  # Update global var

    def btn_new_list_clicked(self):
        """Create a new list based on the sping box. Reset results."""
        x = self.spinBox.value()
        self.ss_num_list = list(range(1, x + 1))
        self.ss_unpicked_list = self.ss_num_list
        self.ss_picked_list = []
        self.update_labels()

    def update_labels(self, current_num=0):
        """Update labels based on current lists."""
        if self.ss_picked_list:
            pl = self.list_to_string(self.ss_picked_list)
            self.ss_picked_list_label.setText(pl)
        else:
            self.ss_picked_list_label.setText("No results.")

        if self.ss_unpicked_list:
            upl = self.list_to_string(self.ss_unpicked_list)
            self.ss_unpicked_list_label.setText(upl)
        else:
            self.ss_unpicked_list_label.setText("All students picked.")

        if current_num == 0:
            self.picked_student_label.setText("--")
        else:
            self.picked_student_label.setText(str(current_num))

    def list_to_string(self, this_list):
        string = " ".join(list(map(str, this_list)))
        return string


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
