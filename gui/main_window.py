from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton,
                              QTableWidget, QTableWidgetItem,
                              QMessageBox, QHeaderView, QApplication)
from PyQt5.QtCore import Qt, QTimer
import sys
sys.path.append('..')
from generator import generate_password, check_strength
from ml_strength import ml_check_strength
from breach import is_breached
from database import add_password, get_all_passwords, delete_password
from crypto import encrypt_password, decrypt_password
from gui.strength_bar import StrengthBar

class MainWindow(QWidget):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.setWindowTitle("Password Manager — Vault")
        self.setMinimumSize(700, 500)
        self.setup_ui()
        self.load_passwords()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # --- Title ---
        title = QLabel("Your Password Vault")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # --- Add password form ---
        form_layout = QHBoxLayout()

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Website (e.g. gmail.com)")
        self.site_input.setFixedHeight(34)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username / Email")
        self.user_input.setFixedHeight(34)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setFixedHeight(34)
        self.pass_input.textChanged.connect(self.on_password_typed)

        self.add_btn = QPushButton("Add")
        self.add_btn.setFixedHeight(34)
        self.add_btn.setStyleSheet(
            "background-color: #2563eb; color: white; "
            "border-radius: 6px; font-weight: bold; padding: 0 16px;"
        )
        self.add_btn.clicked.connect(self.add_entry)

        self.gen_btn = QPushButton("Generate")
        self.gen_btn.setFixedHeight(34)
        self.gen_btn.setStyleSheet(
            "border-radius: 6px; padding: 0 12px;"
        )
        self.gen_btn.clicked.connect(self.generate_password)

        form_layout.addWidget(self.site_input)
        form_layout.addWidget(self.user_input)
        form_layout.addWidget(self.pass_input)
        form_layout.addWidget(self.gen_btn)
        form_layout.addWidget(self.add_btn)
        main_layout.addLayout(form_layout)

        # --- Strength bar ---
        self.strength_bar = StrengthBar()
        main_layout.addWidget(self.strength_bar)

        # --- Password table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def on_password_typed(self, text):
        if text:
            strength = ml_check_strength(text)
            self.strength_bar.update_strength(strength)

    def generate_password(self):
        password = generate_password(length=16)
        self.pass_input.setText(password)

    def add_entry(self):
        site = self.site_input.text().strip()
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not site or not username or not password:
            QMessageBox.warning(self, "Missing info",
                                "Please fill in all three fields.")
            return

        if is_breached(password):
            QMessageBox.warning(self, "Breached Password",
                                "This password was found in known breaches. "
                                "Please choose a stronger one.")
            return

        encrypted = encrypt_password(password, self.key)
        add_password(site, username, encrypted)

        self.site_input.clear()
        self.user_input.clear()
        self.pass_input.clear()
        self.strength_bar.bar.setValue(0)
        self.strength_bar.label.setText("Strength: —")
        self.load_passwords()

    def load_passwords(self):
        self.table.setRowCount(0)
        entries = get_all_passwords()
        for entry_id, site, username, encrypted in entries:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(site))
            self.table.setItem(row, 1, QTableWidgetItem(username))
            self.table.setItem(row, 2, QTableWidgetItem("••••••••"))

            # Action buttons
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            copy_btn = QPushButton("Copy")
            copy_btn.setStyleSheet(
                "background-color: #16a34a; color: white; "
                "border-radius: 4px; padding: 2px 8px;"
            )
            copy_btn.clicked.connect(
                lambda _, eid=entry_id, enc=encrypted: 
                self.copy_password(eid, enc)
            )

            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet(
                "background-color: #dc2626; color: white; "
                "border-radius: 4px; padding: 2px 8px;"
            )
            del_btn.clicked.connect(
                lambda _, eid=entry_id: self.delete_entry(eid)
            )

            btn_widget = QWidget()
            btn_layout.addWidget(copy_btn)
            btn_layout.addWidget(del_btn)
            btn_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 3, btn_widget)

    def copy_password(self, entry_id, encrypted):
        try:
            password = decrypt_password(encrypted, self.key)
            clipboard = QApplication.clipboard()
            clipboard.setText(password)

            # Auto-clear clipboard after 30 seconds
            QTimer.singleShot(
                30000,
                lambda: clipboard.setText("")
            )
            QMessageBox.information(self, "Copied",
                                    "Password copied! Clipboard clears in 30 seconds.")
        except Exception:
            QMessageBox.critical(self, "Error",
                                 "Could not decrypt password.")

    def delete_entry(self, entry_id):
        confirm = QMessageBox.question(
            self, "Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_password(entry_id)
            self.load_passwords()