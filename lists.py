# TODO:
# Change QListWidget to use QListView
# Create QStringListModel for this purpose
# This should make it easier to manipulate the lists in the end

import random
import os
import utils

from PyQt6.QtCore import (
    QSize, Qt, QStringListModel, QEvent, QPropertyAnimation,
    QEasingCurve, QSequentialAnimationGroup, QPoint, QParallelAnimationGroup
)
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
    QListView,
    QMenu,
    QComboBox,
    QCheckBox,
    QGraphicsOpacityEffect,
)
from PyQt6.QtGui import QFont, QPalette, QColor, QAction, QContextMenuEvent


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
        self.picked_student_label = QLabel("--")
        self.picked_student_label.setObjectName("picked_student_label")
        self.picked_student_label.setFont(result_font)
        self.btn_pick_clicked_restart_flag = 0
        self.last_picked_num = 0

        # Saved lists setup
        self.saved_lists = utils.load_lists()

        # Fairness settings
        self.pick_counts = {}
        self.cb_fairness = QCheckBox("Fairness Mode")
        self.cb_fairness.setToolTip("Students picked in previous rounds are less likely to be picked again.")
        self.cb_fairness.stateChanged.connect(self.on_fairness_toggled)

        # Animation setup
        self.opacity_effect = QGraphicsOpacityEffect()
        self.picked_student_label.setGraphicsEffect(self.opacity_effect)

        # Create buttons before layouts.
        self.create_buttons()

        topLeftLayout = self.createTopLeftLayout(def_ss, max_ss)
        # topRightLayout = self.createTopRightLayout()
        bottomLayout = self.createBottomLayout()

        # Main Layout
        mainLayout = QGridLayout()
        # mainLayout.setColumnStretch(0, 3) # Relic from 2 column layout
        # mainLayout.setColumnStretch(1, 1)
        mainLayout.addLayout(topLeftLayout, 0, 0)
        # mainLayout.addLayout(topRightLayout, 0, 1)
        mainLayout.addLayout(bottomLayout, 1, 0)

        self.setLayout(mainLayout)

    def createTopLeftLayout(self, def_ss, max_ss):
        topLeftLayout = QVBoxLayout()
        topLeftGroupBox1 = QGroupBox("Chosen Student")
        topLeftGroupBox1.setMinimumHeight(180)
        topLeftGroupBox1Layout = QVBoxLayout()
        topLeftGroupBox1.setLayout(topLeftGroupBox1Layout)

        # Container for the label to allow animation
        self.label_container = QWidget()
        self.label_container.setMinimumHeight(140)
        # We don't use a layout for the container to allow absolute positioning of the label
        self.picked_student_label.setParent(self.label_container)
        self.picked_student_label.setFixedWidth(400)
        self.picked_student_label.move(0, 20)

        topLeftGroupBox1Layout.addWidget(self.label_container)

        guideText = QLabel(
            "Click create to replace the list. You can add or remove specific "
            "students. Restarting will keep these changes.",
            wordWrap=1,
            margin=10,
        )
        guideText.setObjectName("guide_text")

        # topLeftLayout.addWidget(topLeftGroupBox1) # Move this down
        topLeftLayout.setContentsMargins(10, 10, 10, 10)

        # Create a textbox for a new list.
        self.create_list_textbox = QPlainTextEdit(maximumWidth=1000)
        self.create_list_textbox.setPlainText("George, Harry Smith, Sarah, Mina")

        # Create a textbox for adding or removing students.
        self.add_remove_textbox = QLineEdit(maximumWidth=1000)
        self.add_remove_textbox.setPlaceholderText("Type student name...")
        self.add_remove_textbox.returnPressed.connect(self.btn_add_student_clicked)

        # Create student lists.
        topRightLayout = self.createTopRightLayout()

        # Add widgets in order
        topLeftLayout.addWidget(topLeftGroupBox1)
        topLeftLayout.addLayout(topRightLayout)

        # Create a layout for add/remove ss.
        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(self.add_remove_textbox)
        add_remove_layout.addWidget(self.btn_add_student)
        add_remove_layout.addWidget(self.btn_new_list_dialog)
        add_remove_layout.setContentsMargins(0, 10, 0, 0)
        topLeftLayout.addLayout(add_remove_layout)

        # Create a layout for saved lists.
        saved_lists_layout = QHBoxLayout()
        saved_lists_layout.addWidget(self.list_picker)
        saved_lists_layout.addWidget(self.btn_save_list)
        saved_lists_layout.addWidget(self.btn_delete_list)
        saved_lists_layout.setContentsMargins(0, 5, 0, 0)
        topLeftLayout.addLayout(saved_lists_layout)

        # Fairness checkbox
        topLeftLayout.addWidget(self.cb_fairness)

        return topLeftLayout

    def createTopRightLayout(self):  # Student lists. (Was top right.)
        # Top right box - lists and results
        topRightLayout = QHBoxLayout()

        # --- Unpicked students group box
        self.unpicked_group_box = QGroupBox("Unpicked Students")
        topRightGroupBox1Layout = QVBoxLayout()
        self.ss_unpicked_list_view = QListView()
        self.ss_unpicked_list_view.customContextMenuRequested.connect(self.unpicked_list_menu)
        self.ss_unpicked_list_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )  # Set right click menu to actions

        self.btn_new_list_clicked()  # To init sample list

        self.unpicked_group_box.setLayout(topRightGroupBox1Layout)
        topRightGroupBox1Layout.addWidget(self.ss_unpicked_list_view)
        topRightLayout.addWidget(self.unpicked_group_box)

        # --- Picked students group box
        self.picked_group_box = QGroupBox("Picked Students")
        topRightGroupBox2Layout = QVBoxLayout()
        self.ss_picked_list_view = QListView()
        self.ss_picked_list_view.customContextMenuRequested.connect(self.picked_list_menu)
        self.ss_picked_list_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )  # Set right click menu to use custom
        self.create_string_models()  # Has to be after creating sample list
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_view)
        self.picked_group_box.setLayout(topRightGroupBox2Layout)
        topRightLayout.addWidget(self.picked_group_box)

        return topRightLayout

    def createBottomLayout(self):
        # Bottom box - big button
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(10, 0, 10, 10)
        bottomLayout.addWidget(self.btn_pick, 1)
        bottomLayout.addWidget(self.btn_restart, 1)

        return bottomLayout

    def create_string_models(self):
        """Create a model of names to provide strings to views."""
        self.ss_unpicked_model = QStringListModel(self.ss_name_list)
        self.ss_unpicked_list_view.setModel(self.ss_unpicked_model)  # Apply model
        self.ss_picked_model = QStringListModel()
        self.ss_picked_list_view.setModel(self.ss_picked_model)
        self.btn_pick_enable_check()

    def create_buttons(self):
        """Create buttons for the main window."""
        self.btn_pick = QPushButton("Pick a Student", maximumWidth=500)
        self.btn_pick.setObjectName("btn_pick")
        self.btn_pick.clicked.connect(self.btn_pick_clicked)

        self.btn_restart = QPushButton("🔄 Restart", maximumWidth=500)
        self.btn_restart.setObjectName("btn_restart")
        self.btn_restart.clicked.connect(self.btn_restart_clicked)

        self.btn_new_list = QPushButton("✨ Create", maximumWidth=100)
        self.btn_new_list.clicked.connect(self.btn_new_list_clicked)

        self.btn_new_list_dialog = QPushButton("📝 Create New List", maximumWidth=250)
        self.btn_new_list_dialog.clicked.connect(self.btn_new_list_dialog_clicked)

        self.btn_add_student = QPushButton("➕ Add", maximumWidth=80)
        self.btn_add_student.clicked.connect(self.btn_add_student_clicked)

        self.btn_save_list = QPushButton("💾 Save Current", maximumWidth=130)
        self.btn_save_list.clicked.connect(self.save_list_clicked)

        self.btn_delete_list = QPushButton("🗑️ Delete", maximumWidth=100)
        self.btn_delete_list.clicked.connect(self.delete_list_clicked)

        self.list_picker = QComboBox()
        self.list_picker.currentIndexChanged.connect(self.load_selected_list)
        self.update_list_picker()

    def btn_add_student_clicked(self):
        """Add the student to the current list and update all lists."""
        x = self.add_remove_textbox.text().strip()
        if x not in self.ss_name_list:
            self.ss_name_list.append(x)
            self.model_insert_name(self.ss_unpicked_model, x)
            self.ss_unpicked_model.sort(0)  # 0 = column
        self.add_remove_textbox.clear()

    def model_insert_name(self, model, name):
        """Insert a name at the top of the passed model."""
        model.insertRow(0)
        index = model.index(0)
        model.setData(index, name)

    def btn_pick_clicked(self):
        """Pick a student from the list, show result (and remove)."""
        if self.cb_fairness.isChecked():
            # In Fairness mode, we pick from the full set and don't move between lists.
            all_students = self.ss_name_list
            if not all_students:
                return

            weights = []
            for student in all_students:
                count = self.pick_counts.get(student, 0)
                weight = 1.0 / (1.0 + count)
                weights.append(weight)

            picked = random.choices(all_students, weights=weights, k=1)[0]
            self.pick_counts[picked] = self.pick_counts.get(picked, 0) + 1
            self.run_pick_animation(picked)
        else:
            rowCount = self.ss_unpicked_model.rowCount()  # Get size of list
            print(f"NumRows: {rowCount}")

            if rowCount <= 0:
                return

            randomValue = random.randrange(0, rowCount)  # Pick random
            index = self.ss_unpicked_model.index(randomValue)  # Get index of picked
            picked = self.ss_unpicked_model.data(index)  # Get picked string

            print(f"Selected: {randomValue}")
            print(f"Index data:{picked}")
            self.ss_unpicked_model.removeRows(randomValue, 1)  # Remove picked
            self.model_insert_name(self.ss_picked_model, picked)
            self.last_picked_num = randomValue
            self.run_pick_animation(picked)
            self.btn_pick_enable_check()

    def run_pick_animation(self, name):
        """Animate the student name sliding out to bottom and sliding in from top."""
        # Current centered position is roughly (0, 20) in the 140px container
        curr_x = self.picked_student_label.x()

        # 1. Slide Out (to bottom)
        self.exit_anim = QPropertyAnimation(self.picked_student_label, b"pos")
        self.exit_anim.setDuration(120)
        self.exit_anim.setStartValue(QPoint(curr_x, 20))
        self.exit_anim.setEndValue(QPoint(curr_x, 100))
        self.exit_anim.setEasingCurve(QEasingCurve.Type.InQuad)

        self.exit_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.exit_opacity.setDuration(120)
        self.exit_opacity.setStartValue(1.0)
        self.exit_opacity.setEndValue(0.0)

        self.exit_group = QParallelAnimationGroup()
        self.exit_group.addAnimation(self.exit_anim)
        self.exit_group.addAnimation(self.exit_opacity)

        # 2. Update Text and Reset Position (during the transition)
        def update_text():
            self.picked_student_label.setText(name)
            self.picked_student_label.move(curr_x, -60)

        self.exit_group.finished.connect(update_text)

        # 3. Slide In (from top)
        self.enter_anim = QPropertyAnimation(self.picked_student_label, b"pos")
        self.enter_anim.setDuration(220)
        self.enter_anim.setStartValue(QPoint(curr_x, -60))
        self.enter_anim.setEndValue(QPoint(curr_x, 20))
        self.enter_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.enter_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.enter_opacity.setDuration(180)
        self.enter_opacity.setStartValue(0.0)
        self.enter_opacity.setEndValue(1.0)

        self.enter_group = QParallelAnimationGroup()
        self.enter_group.addAnimation(self.enter_anim)
        self.enter_group.addAnimation(self.enter_opacity)

        self.seq_group = QSequentialAnimationGroup()
        self.seq_group.addAnimation(self.exit_group)
        self.seq_group.addAnimation(self.enter_group)
        self.seq_group.start()

    def btn_new_list_clicked(self):  # Perhaps redundant but still used on startup
        """Create a new list based on the text box. Reset results."""
        x = self.create_list_textbox.toPlainText()
        x = set(x.split(","))
        x = [z.strip() for z in x]
        x = list(filter(None, x))
        self.ss_name_list = x.copy()
        self.ss_unpicked_list = self.ss_name_list.copy()
        self.ss_picked_list = []
        self.picked_student_label.setText("--")

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
            x = self.clean_list(x)
            print(x)
            x.sort()
            self.ss_name_list = x.copy()
            self.create_string_models()
            self.reset_fairness_counts()
            self.picked_student_label.setText("--")

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

        self.btn_pick_enable_check()

    def reset_fairness_counts(self):
        """Reset the counts for fairness mode."""
        self.pick_counts = {}
        print("Fairness counts reset.")

    def unpicked_list_menu(self, position):
        selected = self.ss_unpicked_list_view.currentIndex()
        selected_name = self.ss_unpicked_model.data(selected)

        cmenu = QMenu()
        pick = cmenu.addAction("Pick selected")
        remove = cmenu.addAction("Remove")
        action = cmenu.exec(self.ss_unpicked_list_view.mapToGlobal(position))

        rowCount = self.ss_unpicked_model.rowCount()

        print(f"Row count:{rowCount}")

        if rowCount <= 0: # If list empty do nothing
            pass
        elif action == pick:
            print("PICK IT")
            for n in range(rowCount): # Find the row to remove
                if self.ss_unpicked_model.index(n) == selected:
                    self.ss_unpicked_model.removeRows(n, 1)

            self.model_insert_name(self.ss_picked_model, selected_name)

        elif action == remove:
            print("REMOVE")
            for n in range(rowCount): # Find the row to remove
                if self.ss_unpicked_model.index(n) == selected:
                    self.ss_unpicked_model.removeRows(n, 1)

        self.btn_pick_enable_check()
        self.update_name_list()

    def picked_list_menu(self, position):
        selected = self.ss_picked_list_view.currentIndex()
        selected_name = self.ss_picked_model.data(selected)

        cmenu = QMenu()
        unpick = cmenu.addAction("Unpick selected")
        remove = cmenu.addAction("Remove")
        action = cmenu.exec(self.ss_picked_list_view.mapToGlobal(position))

        rowCount = self.ss_picked_model.rowCount()

        print(f"Row count:{rowCount}")

        if rowCount <= 0: # If list empty do nothing
            pass
        elif action == unpick:
            print("PICK IT")
            for n in range(rowCount): # Find the row to remove
                if self.ss_picked_model.index(n) == selected:
                    self.ss_picked_model.removeRows(n, 1)

            self.model_insert_name(self.ss_unpicked_model, selected_name)

        elif action == remove:
            print("REMOVE")
            for n in range(rowCount): # Find the row to remove
                if self.ss_picked_model.index(n) == selected:
                    self.ss_picked_model.removeRows(n, 1)

        self.btn_pick_enable_check()
        self.update_name_list()

    def clean_list(self, x):
        """Remove dups, whitespace and empty strings from a list."""
        x = [z.strip() for z in x]  # Remove whitespace
        x = set(x)  # Remove duplicates
        x = list(filter(None, x))  # Remove empty strings and return to list
        x.sort()
        return x

    def btn_restart_clicked(self):
        """Restart the lists based on current list."""
        combined = self.update_name_list()
        self.ss_name_list = combined.copy()  # Update global variable.
        self.create_string_models()  # Recreate models based on combined list.
        self.btn_pick_enable_check()

    def update_name_list(self):
        """Updates simple name list to match model of both lists."""
        picked = self.ss_picked_model.stringList()
        unpicked = self.ss_unpicked_model.stringList()
        combined = picked + unpicked
        print(f"Combined: {combined}")
        combined = self.clean_list(combined)
        print(f"Combined Dups: {combined}")
        self.ss_name_list = combined.copy()  # Update global variable.
        return combined

    def btn_pick_enable_check(self):
        """Check if the pick button should be enabled or disabled."""
        unpicked_rows = self.ss_unpicked_model.rowCount()
        picked_rows = self.ss_picked_model.rowCount()
        print(unpicked_rows)
        print(picked_rows)

        if self.ss_unpicked_model.rowCount() >= 1 or self.cb_fairness.isChecked():
            self.btn_pick.setEnabled(1)
        else:
            self.btn_pick.setDisabled(1)

        if self.ss_picked_model.rowCount() >= 1 and not self.cb_fairness.isChecked():
            self.btn_restart.setEnabled(1)
        elif self.cb_fairness.isChecked():
            self.btn_restart.setEnabled(0) # Restart doesn't make sense if everyone is always there
        else:
            self.btn_restart.setDisabled(1)

    def list_to_string(self, this_list):
        string = ", ".join(list(map(str, this_list)))
        return string

    def showEvent(self, event):
        """Reload lists from file when the tab is shown."""
        super().showEvent(event)
        current_selection = self.list_picker.currentText()
        self.saved_lists = utils.load_lists()
        self.update_list_picker()

        # Restore selection if it still exists
        index = self.list_picker.findText(current_selection)
        if index >= 0:
            self.list_picker.setCurrentIndex(index)
            # Re-load the list to ensure it's fresh
            self.load_selected_list(index)

    def save_lists_to_file(self):
        """Save current dictionary of lists to JSON file."""
        utils.save_lists(self.saved_lists)

    def update_list_picker(self):
        """Populate the list picker combo box with saved list names."""
        self.list_picker.blockSignals(True)
        self.list_picker.clear()
        self.list_picker.addItem("Select a saved list...")
        for name in sorted(self.saved_lists.keys()):
            self.list_picker.addItem(name)
        self.list_picker.blockSignals(False)

    def save_list_clicked(self):
        """Prompt user for a name and save current name list."""
        name, ok = QInputDialog.getText(self, "Save List", "Enter list name:")
        if ok and name:
            self.update_name_list()  # Ensure ss_name_list is current
            self.saved_lists[name] = self.ss_name_list
            self.save_lists_to_file()
            self.update_list_picker()
            # Select the newly saved list
            index = self.list_picker.findText(name)
            if index >= 0:
                self.list_picker.setCurrentIndex(index)

    def delete_list_clicked(self):
        """Delete the currently selected list from saved lists."""
        name = self.list_picker.currentText()
        if name != "Select a saved list...":
            self.saved_lists.pop(name, None)
            self.save_lists_to_file()
            self.update_list_picker()

    def load_selected_list(self, index):
        """Load the selected list from the picker."""
        name = self.list_picker.itemText(index)
        if name in self.saved_lists:
            self.ss_name_list = self.saved_lists[name].copy()
            self.create_string_models()
            self.reset_fairness_counts()
            self.picked_student_label.setText("--")
