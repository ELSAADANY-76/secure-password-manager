from sklearn.ensemble import RandomForestClassifier
import string

def extract_features(password: str) -> list:
    """Turn a password into numbers the ML model can understand."""
    length = len(password)
    has_upper = int(any(c.isupper() for c in password))
    has_lower = int(any(c.islower() for c in password))
    has_digit = int(any(c.isdigit() for c in password))
    has_symbol = int(any(c in string.punctuation for c in password))
    unique_chars = len(set(password))
    digit_count = sum(1 for c in password if c.isdigit())
    symbol_count = sum(1 for c in string.punctuation if c in password)
    upper_count = sum(1 for c in password if c.isupper())

    return [
        length,
        has_upper,
        has_lower,
        has_digit,
        has_symbol,
        unique_chars,
        digit_count,
        symbol_count,
        upper_count
    ]

def train_model() -> RandomForestClassifier:
    """Train a Random Forest model on password examples."""
    # Training data — [password, label]
    # Labels: 0 = Weak, 1 = Medium, 2 = Strong
    training_passwords = [
        # Weak passwords
        ("123456", 0),
        ("password", 0),
        ("abc123", 0),
        ("qwerty", 0),
        ("111111", 0),
        ("iloveyou", 0),
        ("monkey", 0),
        ("dragon", 0),
        ("123456789", 0),
        ("letmein", 0),
        ("sunshine", 0),
        ("princess", 0),
        ("welcome", 0),
        ("shadow", 0),
        ("superman", 0),
        ("michael", 0),
        ("football", 0),
        ("pass", 0),
        ("1234", 0),
        ("test", 0),

        # Medium passwords
        ("Password1", 1),
        ("Hello123!", 1),
        ("Summer2023", 1),
        ("Blue_Sky99", 1),
        ("Python2024", 1),
        ("MyPass123", 1),
        ("Cairo2024!", 1),
        ("Orange#99", 1),
        ("Delta456!", 1),
        ("Rocket789", 1),
        ("Galaxy123", 1),
        ("Falcon_22", 1),
        ("Thunder55!", 1),
        ("Winter2023", 1),
        ("Alpha_123", 1),
        ("Silver88!", 1),
        ("Gamma2024", 1),
        ("Neptune11", 1),
        ("Cookie_42", 1),
        ("Laptop789", 1),

        # Strong passwords
        ("X#9kL!mP2@qR", 2),
        ("Tr0ub4dor&3", 2),
        ("C0rr3ct!H0rs3", 2),
        ("P@ssw0rd#2024!", 2),
        ("Zx!9Lm@3Kp#7", 2),
        ("Qw3rty!@#456Zx", 2),
        ("Hy#8Lp!2Mn@9", 2),
        ("Vk!3Wx@7Yz#1", 2),
        ("Jt@5Rn!8Ks#2", 2),
        ("Nb!6Qm@4Lp#9", 2),
        ("Fg#2Ht!5Jk@8", 2),
        ("Wd@7Xs!3Yv#6", 2),
        ("Rp!9Tq@2Us#4", 2),
        ("Mn#5Ow!7Px@1", 2),
        ("Lk@3Nm!6Oq#8", 2),
        ("Ij!4Kl@9Mn#2", 2),
        ("Gh#7Hi!1Jk@5", 2),
        ("Ef@2Fg!8Gh#3", 2),
        ("Cd!6De@4Ef#9", 2),
        ("Ab#1Bc!5Cd@7", 2),
    ]

    X = [extract_features(p) for p, _ in training_passwords]
    y = [label for _, label in training_passwords]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# Train model once when the file is imported
_model = train_model()

def ml_check_strength(password: str) -> str:
    """Use the ML model to predict password strength."""
    if not password:
        return 'Weak'
    features = extract_features(password)
    prediction = _model.predict([features])[0]
    if prediction == 0:
        return 'Weak'
    elif prediction == 1:
        return 'Medium'
    else:
        return 'Strong'