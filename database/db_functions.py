from .db_connection import get_connection

def authenticate_user(username, password, user_type):
    table = "doctors" if user_type.lower() == "doctor" else "patients"
    query = f"SELECT * FROM {table} WHERE name=%s AND password=%s"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def register_user(username, password, phone, user_type):
    table = "doctors" if user_type.lower() == "doctor" else "patients"
    query = f"INSERT INTO {table} (name, password, phone_number) VALUES (%s, %s, %s)"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (username, password, phone))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Registration Error:", e)
        return False
