from .db_connection import get_connection
from crypto import encrypt_data, decrypt_data

def authenticate_user(username, password, user_type):
    table = "doctors" if user_type.lower() == "doctor" else "patients"
    query = f"SELECT * FROM {table}"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    for record in records:
        decrypted_name = decrypt_data(record['name'])
        decrypted_password = decrypt_data(record['password'])

        if decrypted_name == username and decrypted_password == password:
            # Decrypt all other fields in the record before returning (optional)
            record['name'] = decrypted_name
            record['password'] = decrypted_password
            if 'phone' in record:
                record['phone'] = decrypt_data(record['phone'])
            return record

    return None


def register_user(username, password, phone, user_type):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        table = "doctors" if user_type.lower() == "doctor" else "patients"

        # Check if the username already exists
        cursor.execute(f"SELECT name FROM {table}")
        existing_usernames = cursor.fetchall()

        for (encrypted_name,) in existing_usernames:
            decrypted_name = decrypt_data(encrypted_name)
            if decrypted_name == username:
                return "exists"

        # Encrypt the input values
        encrypted_username = encrypt_data(username)
        encrypted_password = encrypt_data(password)
        encrypted_phone = encrypt_data(phone)

        # Insert new user
        insert_query = f"INSERT INTO {table} (name, password, phone) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (encrypted_username, encrypted_password, encrypted_phone))
        conn.commit()

        return "success"

    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
        return "error"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


