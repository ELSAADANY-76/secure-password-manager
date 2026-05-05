import hashlib

COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "qwerty", "abc123", "football", "monkey",
    "letmein", "shadow", "master", "dragon", "111111",
    "baseball", "iloveyou", "trustno1", "sunshine", "princess"
]

def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

def is_breached(password: str) -> bool:
    hashed = hash_password(password)
    for common in COMMON_PASSWORDS:
        if hashed == hash_password(common):
            return True
    return False