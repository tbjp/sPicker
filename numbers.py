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
    QSpinBox,
    QLabel,
    QGroupBox,
    QTabWidget,
    QStyleFactory,
    QCheckBox,
)
from PyQt6.QtGui import QFont, QPalette, QColor


class Numbers(QWidget):
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
        self.ss_num_list = list(range(1, def_ss))
        self.ss_picked_list = []
        self.resultsString = ""
        self.ss_unpicked_list_label = QLabel("Empty List", wordWrap=1000)
        self.picked_student_label = QLabel("--")
        self.picked_student_label.setObjectName("picked_student_label")
        self.picked_student_label.setFont(result_font)
        self.btn_pick_clicked_restart_flag = 0
        self.last_picked_num = 0

        # Fairness settings
        self.pick_counts = {}
        self.cb_fairness = QCheckBox("Fairness Mode")
        self.cb_fairness.setToolTip("Students picked in previous rounds are less likely to be picked again.")
        self.cb_fairness.stateChanged.connect(self.on_fairness_toggled)

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

        guideText.setObjectName("guide_text")
        topLeftLayout.addWidget(topLeftGroupBox1)
        topLeftLayout.addWidget(guideText)
        topLeftLayout.setContentsMargins(10, 10, 10, 10)

        # Create a spinbox for a new list.
        self.create_list_spinbox = QSpinBox(maximumWidth=100)
        self.create_list_spinbox.setValue(def_ss)
        self.create_list_spinbox.setMinimum(1)
        self.create_list_spinbox.setMaximum(max_ss)

        # Create a spinbox for adding or removing students.
        self.add_remove_spinbox = QSpinBox(maximumWidth=100)
        self.add_remove_spinbox.setValue(1)
        self.add_remove_spinbox.setMinimum(1)
        self.add_remove_spinbox.setMaximum(max_ss)

        # Create a layout for the create list spinbox and button.
        create_list_layout = QHBoxLayout()
        create_list_layout.addWidget(self.create_list_spinbox)
        create_list_layout.addWidget(self.btn_new_list)
        create_list_layout.setContentsMargins(50, 10, 50, 10)
        topLeftLayout.addLayout(create_list_layout)

        # Create a layout for add/remove ss.
        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(self.add_remove_spinbox)
        add_remove_layout.addWidget(self.btn_add_student)
        add_remove_layout.addWidget(self.btn_remove_student)
        add_remove_layout.setContentsMargins(10, 10, 10, 10)
        topLeftLayout.addLayout(add_remove_layout)

        # Fairness checkbox
        topLeftLayout.addWidget(self.cb_fairness)

        return topLeftLayout

    def createTopRightLayout(self):
        # Top right box - lists and results
        topRightLayout = QVBoxLayout()

        # --- Unpicked students group box
        self.unpicked_group_box = QGroupBox("Unpicked Students")
        topRightGroupBox1Layout = QVBoxLayout()
        self.ss_picked_list_label = QLabel("No results.", wordWrap=1000)
        self.btn_new_list_clicked()
        self.unpicked_group_box.setLayout(topRightGroupBox1Layout)
        topRightGroupBox1Layout.addWidget(self.ss_unpicked_list_label)
        topRightLayout.addWidget(self.unpicked_group_box)

        # --- Picked students group box
        self.picked_group_box = QGroupBox("Picked Students")
        topRightGroupBox2Layout = QVBoxLayout()
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_label)
        self.picked_group_box.setLayout(topRightGroupBox2Layout)
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_label)
        topRightLayout.addWidget(self.picked_group_box)

        self.ss_unpicked_list_label.setMaximumWidth(200)
        self.ss_picked_list_label.setMaximumWidth(200)

        return topRightLayout

    def createBottomLayout(self):
        # Bottom box - big button
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(10, 0, 10, 10)
        bottomLayout.addWidget(self.btn_pick, 1)
        bottomLayout.addWidget(self.btn_restart, 1)

        return bottomLayout

    def create_buttons(self):
        """Create buttons for the main window."""
        self.btn_pick = QPushButton("🎯 Pick a Student", maximumWidth=1000)
        self.btn_pick.setObjectName("btn_pick")
        self.btn_pick.clicked.connect(self.btn_pick_clicked)

        self.btn_restart = QPushButton("🔄 Restart", maximumWidth=1000)
        self.btn_restart.setObjectName("btn_restart")
        self.btn_restart.clicked.connect(self.btn_restart_clicked)

        self.btn_new_list = QPushButton("✨ Create", maximumWidth=100)
        self.btn_new_list.clicked.connect(self.btn_new_list_clicked)

        self.btn_add_student = QPushButton("➕ Add", maximumWidth=100)
        self.btn_add_student.clicked.connect(self.btn_add_student_clicked)

        self.btn_remove_student = QPushButton("➖ Remove", maximumWidth=100)
        self.btn_remove_student.clicked.connect(self.btn_remove_student_clicked)

    def btn_add_student_clicked(self):
        """Add the student to the current list and update all lists."""
        x = self.add_remove_spinbox.value()
        if x not in self.ss_num_list:
            self.ss_num_list.append(x)
            self.ss_unpicked_list.append(x)
        self.ss_unpicked_list.sort()
        self.update_labels(self.last_picked_num)

    def btn_remove_student_clicked(self):
        """Remove the student to the current list and update all lists."""
        x = self.add_remove_spinbox.value()
        if x in self.ss_num_list:
            self.ss_num_list.remove(x)
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

        if x or self.cb_fairness.isChecked():
            rf = 0  # Still students in list or in fairness mode

            if self.cb_fairness.isChecked():
                # Weighted selection from the FULL list
                full_list = self.ss_num_list
                weights = []
                for student in full_list:
                    count = self.pick_counts.get(student, 0)
                    weight = 1.0 / (1.0 + count)
                    weights.append(weight)

                randomValue = random.choices(full_list, weights=weights, k=1)[0]
                # Increment count
                self.pick_counts[randomValue] = self.pick_counts.get(randomValue, 0) + 1
                # In fairness mode, we don't move students.
                self.update_labels(randomValue)
            else:
                randomValue = random.choice(x)
                print(randomValue)
                self.ss_unpicked_list.remove(randomValue)
                self.ss_picked_list.append(randomValue)
                self.update_labels(randomValue)

            self.last_picked_num = randomValue
            print(f"RF: {rf}")

        if not x and rf == 0 and not self.cb_fairness.isChecked():
            rf = 1
            print(f"RF: {rf}")

        if rf == 1 and not self.cb_fairness.isChecked():  # No students in list.
            self.ss_unpicked_list_label.setText("All students picked.")
            self.btn_pick.setDisabled(1)

        self.btn_pick_clicked_restart_flag = rf  # Update global var

    def btn_new_list_clicked(self):
        """Create a new list based on the sping box. Reset results."""
        x = self.create_list_spinbox.value()
        self.ss_num_list = list(range(1, x + 1))
        self.ss_unpicked_list = self.ss_num_list.copy()
        self.ss_picked_list = []
        self.reset_fairness_counts()
        self.update_labels(0)

    def on_fairness_toggled(self, state):
        """Update UI and reset logic when fairness mode is toggled."""
        self.reset_fairness_counts()
        is_checked = self.cb_fairness.isChecked()

        if is_checked:
            self.unpicked_group_box.setTitle("Students")
            self.picked_group_box.hide()
            # Reset lists to full
            self.btn_restart_clicked()
        else:
            self.unpicked_group_box.setTitle("Unpicked Students")
            self.picked_group_box.show()

        self.update_labels(0)

    def reset_fairness_counts(self):
        """Reset the counts for fairness mode."""
        self.pick_counts = {}
        print("Fairness counts reset.")

    def btn_restart_clicked(self):
        """Restart the lists based on current list."""
        self.ss_unpicked_list = self.ss_num_list.copy()
        self.ss_unpicked_list.sort()
        self.ss_picked_list.clear()
        self.update_labels(0)

    def btn_pick_enable_check(self):
        """Check if the pick button should be enabled or disabled."""
        if self.ss_unpicked_list or self.cb_fairness.isChecked():
            self.btn_pick.setEnabled(1)
        else:
            self.btn_pick.setDisabled(1)

        if self.ss_picked_list and not self.cb_fairness.isChecked():
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
        string = "  ".join(list(map(str, this_list)))
        return string
