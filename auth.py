import hashlib
import json
import os
import random
import time

USER_FILE = 'users.json'

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password: str) -> bool:
    """ Validate password strength: At least 8 characters, 
        including numbers and special characters. """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()" for char in password):
        return False
    return True

def register_user(username: str, password: str, role: str):
    """ Register a new user if the username is not already taken. """
    if not validate_password_strength(password):
        return "Password must be at least 8 characters long, with numbers and special characters."
    
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)

    unique_username = f"{username}_{role}"  # Combine username and role
    
    if unique_username in users:
        return "Username with this role already exists."

    # Collect secret question/answer if needed
    secret_question = input("Set a secret question for password recovery: ")
    secret_answer = input("Enter the answer to your secret question: ")

    users[username] = {
        'password': hash_password(password),
        'role': role,  # 'patient' or 'doctor'
        'secret_question': secret_question,
        'secret_answer': hash_password(secret_answer)
    }
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

    return "User registered successfully."

def authenticate_user(username: str, password: str) -> bool:
    """ Authenticate user based on username and password. """
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, 'r') as f:
        users = json.load(f)

    hashed = hash_password(password)
    return username in users and users[username]['password'] == hashed

def generate_otp() -> str:
    """ Generate a one-time password (OTP) for MFA. """
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    return otp

def verify_otp(input_otp: str, otp: str) -> bool:
    """ Verify the OTP entered by the user. """
    return input_otp == otp

def recover_password(username: str, answer: str) -> bool:
    """ Recover password by answering a secret question. """
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, 'r') as f:
        users = json.load(f)

    if username in users:
        correct_answer = users[username]['secret_answer']
        if hash_password(answer) == correct_answer:
            return True
    return False
