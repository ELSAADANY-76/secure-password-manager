# Secure Password Manager

A desktop password manager built with Python and PyQt5 that stores all passwords locally with AES-256-GCM encryption. Passwords never leave your device.

---

## Team Members
- Teammate 1 Lojain — Backend & Security (encryption, database, password generator, breach detection)
- Teammate 2 Selim — Frontend & GUI (login screen, vault window, strength bar, clipboard)

---

## What This App Does
- Encrypts all passwords using AES-256-GCM encryption
- Protects your vault with a master password using PBKDF2 key derivation
- Generates strong random passwords
- Detects breached/weak passwords using offline database checking
- Shows password strength with a visual indicator
- Automatically clears clipboard after 30 seconds for security
- Stores everything locally — no internet connection required

---

## Project Structure
secure-password-manager/
├── main.py              # App entry point
├── crypto.py            # AES-256-GCM encryption and PBKDF2 key derivation
├── database.py          # SQLite vault storage
├── generator.py         # Password generator and strength checker
├── breach.py            # Offline breach detection
├── requirements.txt     # Python dependencies
├── gui/
│   ├── login_screen.py  # Master password login screen
│   ├── main_window.py   # Main vault window
│   └── strength_bar.py  # Password strength indicator

---

## Requirements
- Python 3.8 or higher
- pip

---

## How To Install

**1. Clone the repository:**
git clone https://github.com/ELSAADANY-76/secure-password-manager.git
cd secure-password-manager

**2. Install dependencies:**
pip install PyQt5 pycryptodome

---

## How To Run
python main.py

A login window will appear. The first time you run it, enter any password — this becomes your master password. Keep it safe, there is no way to recover it if forgotten.

---

## How To Use

| Feature | How |
|---|---|
| Add a password | Fill in website, username, password → click Add |
| Generate a password | Click Generate → it fills automatically |
| Copy a password | Click Copy next to any entry |
| Delete a password | Click Delete next to any entry |
| Breach check | Happens automatically when you click Add |

---

## Security Details

| Feature | Implementation |
|---|---|
| Encryption | AES-256-GCM |
| Key derivation | PBKDF2-HMAC-SHA256, 200,000 iterations |
| Storage | Local SQLite database only |
| Clipboard | Auto-cleared after 30 seconds |
| Breach detection | Offline SHA-1 hash comparison |

---

## Dependencies

| Library | Purpose |
|---|---|
| PyQt5 | Desktop GUI framework |
| PyCryptodome | AES-256-GCM encryption |

---

## How To Contribute
1. Clone the repo
2. Create your files
3. Commit with a clear message
4. Push to main branch