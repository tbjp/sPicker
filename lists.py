# TODO:
# Change QListWidget to use QListView
# Create QStringListModel for this purpose
# This should make it easier to manipulate the lists in the end

import random

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QToolTip,
    QPushButton,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QLineEdit,
    QLabel,
    QGroupBox,
    QTabWidget,
    QStyleFactory,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtGui import QFont, QPalette, QColor


class Lists(QWidget):
    """A class to create a tab that use student numbers."""

    def __init__(self, sp_app):
        super().__init__()
        # Settings
        def_ss = 37  # Default num of students
        max_ss = 50  # Max num of students

        # Fonts
        result_font = QFont()
        result_font.setPointSize(50)

        # Initialize variables.
        self.ss_name_list = []
        self.ss_picked_list = []
        self.resultsString = ""
        self.ss_unpicked_list_label = QLabel("Empty List", wordWrap=100)
        self.picked_student_label = QLabel("00")
        self.picked_student_label.setFont(result_font)
        self.btn_pick_clicked_restart_flag = 0
        self.last_picked_num = 0

        # Create buttons before layouts.
        self.create_buttons()

        topLeftLayout = self.createTopLeftLayout(def_ss, max_ss)
        topRightLayout = self.createTopRightLayout()
        bottomLayout = self.createBottomLayout()

        # Main Layout
        mainLayout = QGridLayout()
        mainLayout.setColumnStretch(0, 3)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.addLayout(topLeftLayout, 0, 0)
        mainLayout.addLayout(topRightLayout, 0, 1)
        mainLayout.addLayout(bottomLayout, 1, 0)

        self.setLayout(mainLayout)

    def createTopLeftLayout(self, def_ss, max_ss):
        topLeftLayout = QVBoxLayout()
        topLeftGroupBox1 = QGroupBox("Chosen Student")
        topLeftGroupBox1Layout = QVBoxLayout()
        topLeftGroupBox1.setLayout(topLeftGroupBox1Layout)
        topLeftGroupBox1Layout.addWidget(self.picked_student_label)

        guideText = QLabel(
            "Click create to replace the list. You can add or remove specific "
            "students. Restarting will keep these changes.",
            wordWrap=1,
            margin=10,
        )

        topLeftLayout.addWidget(topLeftGroupBox1)
        topLeftLayout.addWidget(guideText)
        topLeftLayout.setContentsMargins(10, 10, 10, 10)

        # Create a textbox for a new list.
        self.create_list_textbox = QPlainTextEdit(maximumWidth=1000)
        self.create_list_textbox.setPlainText("George, Harry Smith, Sarah, Mina")

        # Create a textbox for adding or removing students.
        self.add_remove_textbox = QLineEdit(maximumWidth=1000)
        self.add_remove_textbox.returnPressed.connect(self.btn_add_student_clicked)

        # Create a layout for the create list textbox and button.
        create_list_layout = QVBoxLayout()
        # create_list_layout.addWidget(self.create_list_textbox)
        # create_list_layout.addWidget(
        #     self.btn_new_list, alignment=Qt.AlignmentFlag.AlignHCenter
        # )
        create_list_layout.addWidget(
            self.btn_new_list_dialog, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        create_list_layout.setContentsMargins(0, 0, 0, 0)
        topLeftLayout.addLayout(create_list_layout)

        # Create a layout for add/remove ss.
        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(self.add_remove_textbox)
        add_remove_layout.addWidget(self.btn_add_student)
        add_remove_layout.addWidget(self.btn_remove_student)
        add_remove_layout.setContentsMargins(0, 10, 0, 10)
        topLeftLayout.addLayout(add_remove_layout)

        return topLeftLayout

    def createTopRightLayout(self):
        # Top right box - lists and results
        topRightLayout = QVBoxLayout()

        # --- Unpicked students group box
        topRightGroupBox1 = QGroupBox("Unpicked Students")
        topRightGroupBox1Layout = QVBoxLayout()
        self.ss_unpicked_list_widget = QListWidget(parent=topRightGroupBox1)
        self.ss_picked_list_label = QLabel("No results.", wordWrap=1000)  # delete
        self.btn_new_list_clicked()
        topRightGroupBox1.setLayout(topRightGroupBox1Layout)
        topRightGroupBox1Layout.addWidget(self.ss_unpicked_list_widget)
        topRightLayout.addWidget(topRightGroupBox1)

        # --- Picked students group box
        topRightGroupBox2 = QGroupBox("Picked Students")
        topRightGroupBox2Layout = QVBoxLayout()
        self.ss_picked_list_widget = QListWidget(parent=topRightGroupBox2)
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_widget)
        topRightGroupBox2.setLayout(topRightGroupBox2Layout)
        topRightLayout.addWidget(topRightGroupBox2)

        return topRightLayout

    def createBottomLayout(self):
        # Bottom box - big button
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.btn_pick)
        bottomLayout.addWidget(self.btn_restart)

        return bottomLayout

    def create_buttons(self):
        """Create buttons for the main window."""
        self.btn_pick = QPushButton("Pick a Student", maximumWidth=1000)
        self.btn_pick.clicked.connect(self.btn_pick_clicked)

        self.btn_restart = QPushButton("Restart", maximumWidth=100)
        self.btn_restart.clicked.connect(self.btn_restart_clicked)

        self.btn_new_list = QPushButton("Create", maximumWidth=100)
        self.btn_new_list.clicked.connect(self.btn_new_list_clicked)

        self.btn_new_list_dialog = QPushButton("Create New List", maximumWidth=250)
        self.btn_new_list_dialog.clicked.connect(self.btn_new_list_dialog_clicked)

        self.btn_add_student = QPushButton("Add", maximumWidth=50)
        self.btn_add_student.clicked.connect(self.btn_add_student_clicked)

        self.btn_remove_student = QPushButton("Remove", maximumWidth=80)
        self.btn_remove_student.clicked.connect(self.btn_remove_student_clicked)

    def btn_add_student_clicked(self):
        """Add the student to the current list and update all lists."""
        x = self.add_remove_textbox.text().strip()
        if x not in self.ss_name_list:
            self.ss_name_list.append(x)
            self.ss_unpicked_list.append(x)
        self.ss_unpicked_list.sort()
        self.update_labels(self.last_picked_num)

    def btn_remove_student_clicked(self):
        """Remove the student to the current list and update all lists."""
        x = self.add_remove_textbox.text().strip()
        if x in self.ss_name_list:
            self.ss_name_list.remove(x)
        if x in self.ss_unpicked_list:
            self.ss_unpicked_list.remove(x)
        if x in self.ss_picked_list:
            self.ss_picked_list.remove(x)
        self.ss_unpicked_list.sort()
        self.update_labels(self.last_picked_num)

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
            self.ss_unpicked_list_widget.takeItem(randomValue)
            self.ss_picked_list.append(randomValue)
            self.ss_picked_list_widget.addItem(randomValue)
            self.update_labels(randomValue)
            self.last_picked_num = randomValue
            print(f"RF: {rf}")

        if not x and rf == 0:
            rf = 1
            print(f"RF: {rf}")

        if rf == 1:  # No students in list.
            self.ss_unpicked_list_label.setText("All students picked.")
            self.btn_pick.setDisabled(1)

        self.btn_pick_clicked_restart_flag = rf  # Update global var

    def btn_new_list_clicked(self):  # Perhaps redundant but still used on startup
        """Create a new list based on the text box. Reset results."""
        x = self.create_list_textbox.toPlainText()
        x = set(x.split(","))
        x = [z.strip() for z in x]
        x = list(filter(None, x))
        self.ss_name_list = x.copy()
        self.ss_unpicked_list = self.ss_name_list.copy()
        self.ss_picked_list = []
        self.update_labels(0)

        # New behaviour
        self.ss_unpicked_list_widget.addItems(self.ss_name_list)

    def btn_new_list_dialog_clicked(self):
        """Open a dialog for user to input list of names."""
        prefill_text = self.list_to_string(self.ss_name_list)
        text, ok = QInputDialog.getText(
            self,
            "Create new list",
            "Type or paste student names here,\nseparated by a comma (,).",
            text=prefill_text,
        )
        if ok:
            x = text
            x = x.split(",")
            x = [z.strip() for z in x]  # Remove whitespace
            x = set(x)  # Remove duplicates
            x = list(filter(None, x))  # Remove empty strings and return to list
            # x = list(set(x))
            print(x)
            x.sort()
            self.ss_name_list = x.copy()
            self.ss_unpicked_list = self.ss_name_list.copy()
            self.ss_picked_list = []
            self.update_labels(0)

            # New behaviour
            self.ss_unpicked_list_widget.clear()
            self.ss_picked_list_widget.clear()
            self.ss_unpicked_list_widget.addItems(self.ss_unpicked_list)

    def btn_restart_clicked(self):
        """Restart the lists based on current list."""
        self.ss_unpicked_list = self.ss_name_list.copy()
        self.ss_unpicked_list.sort()
        self.ss_picked_list.clear()
        self.update_labels(0)

    def btn_pick_enable_check(self):
        """Check if the pick button should be enabled or disabled."""
        if self.ss_unpicked_list:
            self.btn_pick.setEnabled(1)
        else:
            self.btn_pick.setDisabled(1)

        if self.ss_picked_list:
            self.btn_restart.setEnabled(1)
        else:
            self.btn_restart.setDisabled(1)

    def update_labels(self, current_num=0):
        """Update labels and buttons based on current lists."""
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

        self.btn_pick_enable_check()

    def list_to_string(self, this_list):
        string = ", ".join(list(map(str, this_list)))
        return string
