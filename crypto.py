from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved to 'secret.key'.")

def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        raise Exception("Key file not found!")
    
def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

def decrypt_data(token):
    key = load_key()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(token).decode()
        return decrypted
    except Exception as e:
        print("Decryption failed:", e)
        return None