import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import logging

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, phone_number VARCHAR(20) UNIQUE, password_hash CHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"
)


load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(
    dbname="project",
    user="sammy",
    password=5914,
    host="localhost",
    port=5432
)

@app.post("/api/register")
def register_user():
    data = request.get_json()
    email = data.get("email")
    phone_number = data.get("phone_number")  # Optional
    password = data.get("password")

    # Validate user input (consider using a validation library or custom checks)
    if not email or not password:
        return jsonify({"message": "Missing required fields (email and password)."})

    # Improve password validation (optional)
    # Enforce minimum password length (e.g., 8 characters)
    # Require a mix of uppercase, lowercase, numbers, and symbols
    # ... (implement your validation logic here)

    with connection.cursor() as cursor:
        # Check for existing email or phone number (if applicable)
        cursor.execute("SELECT * FROM users WHERE email = %s OR phone_number = %s", (email, phone_number))
        existing_user = cursor.fetchone()
        if existing_user:
            if existing_user[1] == email:
                return jsonify({"message": "Email already exists."})
            else:
                return jsonify({"message": "Phone number already exists."})

        # Hash password before storing
        password_hash = generate_password_hash(password)

        # Insert user data
        cursor.execute(
            "INSERT INTO users (email, phone_number, password_hash) VALUES (%s, %s, %s)",
            (email, phone_number, password_hash),
        )
        connection.commit()

    return jsonify({"message": "User created successfully."}), 201


@app.post("/api/login")
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validate user input (consider using a validation library or custom checks)
    if not email or not password:
        return jsonify({"message": "Missing required fields (email and password)."})

    # Fetch user data by email from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    
    pas = user[3].strip()

    # Check if user exists and validate password hash (if user exists)
    if user:
        if check_password_hash(pas, password):  # user[3] is likely the password_hash column
            logging.warning(f"Login failed for email: '{email}', ")
            return jsonify({"message": "login succesfull."}), 401  # Unauthorized
        else:
            logging.info(f"Login not successful for email: '{email}',password mismatch")
            # Login successful (you can optionally generate a session token or JWT here)
            return jsonify({"message": "Login not successful."}), 200
    else:
        logging.info(f"Login attempt for non-existent email: '{email}'")
        return jsonify({"message": "Invalid login credentials."}), 401


if __name__ == "__main__":
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
    app.run(debug=True)


