from werkzeug.security import generate_password_hash

password = "sammy2020 "  # Password with trailing space
password = password.strip()  # Remove leading/trailing spaces
hashed_password = generate_password_hash(password)

print("Hashed password (trimmed):", hashed_password)
