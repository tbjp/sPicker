import random
import json
import os

from PyQt6.QtCore import QSize, Qt, QStringListModel
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QGroupBox,
    QSpinBox,
    QComboBox,
    QScrollArea,
    QGridLayout,
    QInputDialog,
)
from PyQt6.QtGui import QFont


class Teams(QWidget):
    """A class to create a tab that sorts students into teams."""

    def __init__(self, sp_app):
        super().__init__()

        # Initialize variables
        self.ss_name_list = []
        self.saved_lists_file = os.path.join(os.path.dirname(__file__), "saved_lists.json")
        self.saved_lists = self.load_lists_from_file()

        # Create UI components
        self.create_buttons()
        self.create_inputs()

        # Results area
        self.teams_container = QWidget()
        self.teams_layout = QVBoxLayout(self.teams_container)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.teams_container)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")

        # Layouts
        config_layout = self.create_config_layout()

        main_layout = QVBoxLayout()
        main_layout.addLayout(config_layout)

        results_group = QGroupBox("Generated Teams")
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.scroll_area)
        results_group.setLayout(results_layout)

        main_layout.addWidget(results_group, 1)

        # Bottom button
        bottom_buttons = QHBoxLayout()
        bottom_buttons.addWidget(self.btn_generate, 1)
        main_layout.addLayout(bottom_buttons)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.setLayout(main_layout)

    def create_buttons(self):
        self.btn_generate = QPushButton("🎲 Generate Teams")
        self.btn_generate.setObjectName("btn_pick")  # Use the same styling as 'Pick' button
        self.btn_generate.clicked.connect(self.generate_teams)

        self.btn_new_list_dialog = QPushButton("📝 Edit List")
        self.btn_new_list_dialog.clicked.connect(self.btn_new_list_dialog_clicked)

    def create_inputs(self):
        self.list_picker = QComboBox()
        self.list_picker.currentIndexChanged.connect(self.load_selected_list)
        self.update_list_picker()

        self.team_count_spin = QSpinBox()
        self.team_count_spin.setRange(2, 20)
        self.team_count_spin.setValue(2)

        self.team_count_label = QLabel("Number of Teams:")

        self.student_preview = QLabel("No students selected.")
        self.student_preview.setWordWrap(True)
        self.student_preview.setStyleSheet("color: #8c867a; font-style: italic; font-size: 12px;")

    def create_config_layout(self):
        layout = QGridLayout()

        picker_group = QGroupBox("Student List")
        picker_layout = QVBoxLayout()

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(self.list_picker)
        selector_layout.addWidget(self.btn_new_list_dialog)

        picker_layout.addLayout(selector_layout)
        picker_layout.addWidget(self.student_preview)
        picker_group.setLayout(picker_layout)

        settings_group = QGroupBox("Team Settings")
        settings_layout = QVBoxLayout()

        spin_layout = QHBoxLayout()
        spin_layout.addWidget(self.team_count_label)
        spin_layout.addWidget(self.team_count_spin)

        settings_layout.addLayout(spin_layout)
        settings_layout.addStretch()
        settings_group.setLayout(settings_layout)

        layout.addWidget(picker_group, 0, 0)
        layout.addWidget(settings_group, 0, 1)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)

        return layout

    def load_lists_from_file(self):
        if os.path.exists(self.saved_lists_file):
            try:
                with open(self.saved_lists_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading lists: {e}")
        return {}

    def update_list_picker(self):
        self.list_picker.blockSignals(True)
        self.list_picker.clear()
        self.list_picker.addItem("Select a list...")
        for name in sorted(self.saved_lists.keys()):
            self.list_picker.addItem(name)
        self.list_picker.blockSignals(False)

    def load_selected_list(self, index):
        name = self.list_picker.itemText(index)
        if name in self.saved_lists:
            self.ss_name_list = self.saved_lists[name].copy()
            self.update_preview()
        else:
            self.ss_name_list = []
            self.student_preview.setText("No students selected.")

    def update_preview(self):
        if self.ss_name_list:
            text = ", ".join(self.ss_name_list)
            if len(text) > 100:
                text = text[:97] + "..."
            self.student_preview.setText(f"Students ({len(self.ss_name_list)}): {text}")
        else:
            self.student_preview.setText("No students selected.")

    def btn_new_list_dialog_clicked(self):
        prefill_text = ", ".join(self.ss_name_list)
        text, ok = QInputDialog.getText(
            self, "Edit list", "Enter names separated by comma:", text=prefill_text
        )
        if ok:
            names = [n.strip() for n in text.split(",") if n.strip()]
            self.ss_name_list = names
            self.update_preview()
            self.list_picker.setCurrentIndex(0)

    def generate_teams(self):
        if not self.ss_name_list:
            return

        # Clear previous teams
        while self.teams_layout.count():
            item = self.teams_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        num_teams = self.team_count_spin.value()
        students = self.ss_name_list.copy()
        random.shuffle(students)

        teams = [[] for _ in range(num_teams)]
        for i, student in enumerate(students):
            teams[i % num_teams].append(student)

        for i, team_students in enumerate(teams):
            if not team_students:
                continue
            group = QGroupBox(f"Team {i+1}")
            group_layout = QVBoxLayout()
            names_label = QLabel(", ".join(team_students))
            names_label.setWordWrap(True)
            names_label.setStyleSheet("font-size: 14px; color: #5c5751;")
            group_layout.addWidget(names_label)
            group.setLayout(group_layout)
            self.teams_layout.addWidget(group)

        self.teams_layout.addStretch()
