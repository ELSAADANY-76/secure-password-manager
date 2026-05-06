from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                              QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("Password Manager — Login")
        self.setFixedSize(380, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(12)

        title = QLabel("Password Manager")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; margin-bottom: 10px;"
        )

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter master password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(36)
        self.password_input.returnPressed.connect(self.try_login)

        self.login_btn = QPushButton("Unlock Vault")
        self.login_btn.setFixedHeight(36)
        self.login_btn.clicked.connect(self.try_login)
        self.login_btn.setStyleSheet(
            "background-color: #2563eb; color: white; "
            "border-radius: 6px; font-weight: bold;"
        )

        layout.addWidget(title)
        layout.addWidget(QLabel("Master Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def try_login(self):
        password = self.password_input.text()
        if len(password) < 1:
            QMessageBox.warning(self, "Error", 
                                "Please enter your master password.")
            return
        self.on_login_success(password)