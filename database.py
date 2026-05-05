import sqlite3
import json

DB_PATH = 'vault.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master (
            id INTEGER PRIMARY KEY,
            salt TEXT NOT NULL,
            test_encrypted TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_master(salt: bytes, test_encrypted: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM master')
    cursor.execute(
        'INSERT INTO master (salt, test_encrypted) VALUES (?, ?)',
        (salt.hex(), json.dumps(test_encrypted))
    )
    conn.commit()
    conn.close()

def get_master():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT salt, test_encrypted FROM master')
    row = cursor.fetchone()
    conn.close()
    if row:
        return bytes.fromhex(row[0]), json.loads(row[1])
    return None, None

def add_password(site: str, username: str, encrypted: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO vault (site, username, encrypted_password) VALUES (?, ?, ?)',
        (site, username, json.dumps(encrypted))
    )
    conn.commit()
    conn.close()

def get_all_passwords():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, site, username, encrypted_password FROM vault')
    rows = cursor.fetchall()
    conn.close()
    return [(r[0], r[1], r[2], json.loads(r[3])) for r in rows]

def delete_password(entry_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vault WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()