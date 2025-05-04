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
