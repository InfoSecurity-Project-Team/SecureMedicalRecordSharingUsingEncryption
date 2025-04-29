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

def register_user(username: str, password: str, role: str) -> bool:
    """Register a new user if the username is not already taken.

    Raises:
        ValueError: If the password does not meet strength requirements.
    
    Returns:
        bool: True if registration is successful, False otherwise.
    """
    if not validate_password_strength(password):
        raise ValueError("Password must be at least 8 characters long, with numbers and special characters.")
    
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)

    unique_username = f"{username}_{role}".lower()  # Combine username and role
    
    if unique_username in users:
        print("Username with this role already exists.")
        return False

    users[unique_username] = {
        'password': hash_password(password),
        'role': role,  # 'patient' or 'doctor'
    }
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

    return True

def authenticate_user(username: str, password: str, role: str) -> bool:
    """ Authenticate user based on username and password. """
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, 'r') as f:
        users = json.load(f)

    unique_username = f"{username}_{role}".lower()
    hashed = hash_password(password)
    
    return unique_username in users and users[unique_username]['password'] == hashed

def generate_otp() -> tuple[str, float]:
    """ Generate a one-time password (OTP) for MFA. """
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    timestamp = time.time() #Current time in seconds
    return otp, timestamp

def verify_otp(input_otp: str, otp: str, timestamp: float, expiry_seconds: int = 60) -> bool:
    """ Verify the OTP entered by the user, considering exriry time """
    current_time = time.time()
    if current_time-timestamp>expiry_seconds:
        print("OTP expired.")
        return False
    return input_otp == otp
