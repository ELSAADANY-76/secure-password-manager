import sys
import os
from Crypto.Random import get_random_bytes
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget
from database import init_db, save_master, get_master
from crypto import derive_key, encrypt_password, decrypt_password
from gui.login_screen import LoginScreen
from gui.main_window import MainWindow

class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Password Manager")
        self.setMinimumSize(750, 550)

        init_db()

        self.login_screen = LoginScreen(self.handle_login)
        self.addWidget(self.login_screen)
        self.setCurrentWidget(self.login_screen)

    def handle_login(self, master_password: str):
        salt, test_encrypted = get_master()

        # First time — set up master password
        if salt is None:
            salt = get_random_bytes(32)
            key = derive_key(master_password, salt)
            test_encrypted = encrypt_password("verify", key)
            save_master(salt, test_encrypted)
            self.open_vault(key)
            return

        # Returning user — verify master password
        key = derive_key(master_password, salt)
        try:
            result = decrypt_password(test_encrypted, key)
            if result == "verify":
                self.open_vault(key)
            else:
                QMessageBox.critical(self, "Wrong Password",
                                     "Incorrect master password.")
        except Exception:
            QMessageBox.critical(self, "Wrong Password",
                                 "Incorrect master password.")

    def open_vault(self, key):
        self.main_window = MainWindow(key)
        self.addWidget(self.main_window)
        self.setCurrentWidget(self.main_window)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()