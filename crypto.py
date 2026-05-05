import hashlib
from Crypto.Cipher import AES

def derive_key(master_password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode('utf-8'),
        salt,
        iterations=200000,
        dklen=32
    )
    return key

def encrypt_password(plaintext: str, key: bytes) -> dict:
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return {
        'nonce': cipher.nonce.hex(),
        'tag': tag.hex(),
        'ciphertext': ciphertext.hex()
    }

def decrypt_password(encrypted: dict, key: bytes) -> str:
    cipher = AES.new(
        key,
        AES.MODE_GCM,
        nonce=bytes.fromhex(encrypted['nonce'])
    )
    plaintext = cipher.decrypt_and_verify(
        bytes.fromhex(encrypted['ciphertext']),
        bytes.fromhex(encrypted['tag'])
    )
    return plaintext.decode('utf-8')