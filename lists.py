# TODO:
# Change QListWidget to use QListView
# Create QStringListModel for this purpose
# This should make it easier to manipulate the lists in the end

import random

from PyQt6.QtCore import QSize, Qt, QStringListModel, QEvent
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
        self.picked_student_label = QLabel("00")
        self.picked_student_label.setFont(result_font)
        self.btn_pick_clicked_restart_flag = 0
        self.last_picked_num = 0

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
        topLeftLayout.setContentsMargins(10, 10, 10, 10)

        # Create a textbox for a new list.
        self.create_list_textbox = QPlainTextEdit(maximumWidth=1000)
        self.create_list_textbox.setPlainText("George, Harry Smith, Sarah, Mina")

        # Create a textbox for adding or removing students.
        self.add_remove_textbox = QLineEdit(maximumWidth=1000)
        self.add_remove_textbox.returnPressed.connect(self.btn_add_student_clicked)

        # Create student lists.
        topRightLayout = self.createTopRightLayout()
        topLeftLayout.addLayout(topRightLayout)

        # Create a layout for add/remove ss.
        add_remove_layout = QHBoxLayout()
        add_remove_layout.addWidget(self.add_remove_textbox)
        add_remove_layout.addWidget(self.btn_add_student)
        add_remove_layout.addWidget(self.btn_new_list_dialog)
        add_remove_layout.setContentsMargins(0, 10, 0, 0)
        topLeftLayout.addLayout(add_remove_layout)

        return topLeftLayout

    def createTopRightLayout(self):  # Student lists. (Was top right.)
        # Top right box - lists and results
        topRightLayout = QHBoxLayout()

        # --- Unpicked students group box
        topRightGroupBox1 = QGroupBox("Unpicked Students")
        topRightGroupBox1Layout = QVBoxLayout()
        self.ss_unpicked_list_view = QListView()
        self.ss_unpicked_list_view.customContextMenuRequested.connect(self.unpicked_list_menu)
        self.ss_unpicked_list_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )  # Set right click menu to actions

        self.btn_new_list_clicked()  # To init sample list

        topRightGroupBox1.setLayout(topRightGroupBox1Layout)
        topRightGroupBox1Layout.addWidget(self.ss_unpicked_list_view)
        topRightLayout.addWidget(topRightGroupBox1)

        # --- Picked students group box
        topRightGroupBox2 = QGroupBox("Picked Students")
        topRightGroupBox2Layout = QVBoxLayout()
        self.ss_picked_list_view = QListView()
        self.ss_picked_list_view.customContextMenuRequested.connect(self.picked_list_menu)
        self.ss_picked_list_view.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )  # Set right click menu to use custom
        self.create_string_models()  # Has to be after creating sample list
        topRightGroupBox2Layout.addWidget(self.ss_picked_list_view)
        topRightGroupBox2.setLayout(topRightGroupBox2Layout)
        topRightLayout.addWidget(topRightGroupBox2)

        return topRightLayout

    def createBottomLayout(self):
        # Bottom box - big button
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(10, 0, 10, 0)
        bottomLayout.addWidget(self.btn_pick)
        bottomLayout.addWidget(self.btn_restart)

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

    def btn_add_student_clicked(self):
        """Add the student to the current list and update all lists."""
        x = self.add_remove_textbox.text().strip()
        if x not in self.ss_name_list:
            self.ss_name_list.append(x)
            self.model_insert_name(self.ss_unpicked_model, x)
            self.ss_unpicked_model.sort(0)  # 0 = column

    def model_insert_name(self, model, name):
        """Insert a name at the top of the passed model."""
        model.insertRow(0)
        index = model.index(0)
        model.setData(index, name)

    def btn_pick_clicked(self):
        """Pick a student from the list, show result (and remove)."""
        rowCount = self.ss_unpicked_model.rowCount()  # Get size of list
        print(f"NumRows: {rowCount}")
        randomValue = random.randrange(0, rowCount)  # Pick random
        print(f"Selected: {randomValue}")
        index = self.ss_unpicked_model.index(randomValue)  # Get index of picked
        picked = self.ss_unpicked_model.data(index)  # Get picked string
        print(f"Index data:{picked}")
        self.ss_unpicked_model.removeRows(randomValue, 1)  # Remove picked
        self.model_insert_name(self.ss_picked_model, picked)
        self.last_picked_num = randomValue
        self.picked_student_label.setText(picked)
        self.btn_pick_enable_check()

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
            self.picked_student_label.setText("--")

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

        if self.ss_unpicked_model.rowCount() >= 1:
            self.btn_pick.setEnabled(1)
        else:
            self.btn_pick.setDisabled(1)

        if self.ss_picked_model.rowCount() >= 1:
            self.btn_restart.setEnabled(1)
        else:
            self.btn_restart.setDisabled(1)

    def list_to_string(self, this_list):
        string = ", ".join(list(map(str, this_list)))
        return string
