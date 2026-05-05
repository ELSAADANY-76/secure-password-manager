import random
import string

def generate_password(length=16, use_upper=True, 
                       use_digits=True, use_symbols=True) -> str:
    chars = string.ascii_lowercase
    required = []

    if use_upper:
        chars += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        required.append(random.choice(string.digits))
    if use_symbols:
        chars += string.punctuation
        required.append(random.choice(string.punctuation))

    remaining = [random.choice(chars) 
                 for _ in range(length - len(required))]
    password = required + remaining
    random.shuffle(password)
    return ''.join(password)

def check_strength(password: str) -> str:
    score = 0
    if len(password) >= 8:  score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password):          score += 1
    if any(c.isdigit() for c in password):          score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2: return 'Weak'
    if score <= 3: return 'Medium'
    return 'Strong'