from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = "scrypt:32768:8:1$FOLVSmmcm3ypycL2$9a0284f80c0be5c6ade9596ad8bcaf8f5d8b8ddf0541f3ab2b6a97ad14e03fc05d86d900570024323d99ac24359fc3c78a0b2c292fcc1be112ea6e7a3c7373b0"
  # Print for demonstration purposes only (avoid in production)
print("Hashed password:", hashed_password)

# User enters a password during login
login_password = input("Enter your password: ")

# Verify the password against the stored hash
if check_password_hash(hashed_password, login_password):
    print("Login successful!")
else:
    print("Invalid password. Please try again.")
