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
    try:
        conn = get_connection()
        cursor = conn.cursor()

        table = "doctors" if user_type.lower() == "doctor" else "patients"

        # Check if user already exists
        check_query = f"SELECT * FROM {table} WHERE name=%s"
        cursor.execute(check_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "exists"

        # Insert new user
        insert_query = f"INSERT INTO {table} (name, password, phone) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, phone))
        conn.commit()

        return "success"

    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
        return "error"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

