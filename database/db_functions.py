from .db_connection import get_connection
from crypto import encrypt_data, decrypt_data
import datetime

def authenticate_user(username, password, user_type):
    table = "doctors" if user_type.lower() == "doctor" else "patients"
    id_field = "doctor_id" if user_type.lower() == "doctor" else "patient_id"

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
            record['name'] = decrypted_name
            record['password'] = decrypted_password
            if 'phone' in record:
                record['phone'] = decrypt_data(record['phone'])

            return {
                "id": record[id_field],         # Include doctor_id or patient_id
                "name": record['name'],
                "password": record['password'],
                "phone": record.get('phone', ""),
                "user_type": user_type
            }

    return None



def register_user(username, password, phone, email, user_type):
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

        # Encrypt the input values (except email)
        encrypted_username = encrypt_data(username)
        encrypted_password = encrypt_data(password)
        encrypted_phone = encrypt_data(phone)

        # Insert new user (email is stored as plain text)
        insert_query = f"""
            INSERT INTO {table} (name, password, phone, email)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (encrypted_username, encrypted_password, encrypted_phone, email))
        conn.commit()

        return "success"

    except Exception as e:
        print(f"[ERROR] Registration failed: {e}")
        return "error"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_patient_id_by_name(patient_name):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT patient_id, name FROM patients"
        cursor.execute(query)
        records = cursor.fetchall()

        for record in records:
            decrypted_name = decrypt_data(record['name'])
            if decrypted_name == patient_name:
                return record['patient_id']

        return None  # No match found

    except Exception as e:
        print(f"[ERROR] Failed to get patient ID: {e}")
        return None

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def insert_encrypted_medical_record(
    patient_id, doctor_id, age, gender,
    symptoms: list, diagnosis, additional_notes=""
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Join symptom list into a string (comma-separated or newline-separated)
        symptom_str = ", ".join(symptoms)

        query = """
            INSERT INTO medical_records (
                patient_id, doctor_id, age, gender,
                symptoms, diagnosis, additional_notes, date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            patient_id,
            doctor_id,
            encrypt_data(str(age)),
            gender,
            encrypt_data(symptom_str),
            encrypt_data(diagnosis),
            encrypt_data(additional_notes) if additional_notes else None,
            datetime.datetime.now()
        )

        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Error inserting encrypted medical record:", e)
        return False


def get_decrypted_medical_records(patient_id=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if patient_id:
            query = """
                SELECT mr.record_id, mr.patient_id, mr.doctor_id, d.name AS doctor_name,
                       mr.age, mr.gender, mr.symptoms, mr.diagnosis,
                       mr.additional_notes, mr.date
                FROM medical_records mr
                JOIN doctors d ON mr.doctor_id = d.doctor_id
                WHERE mr.patient_id = %s
            """
            cursor.execute(query, (patient_id,))
        else:
            query = """
                SELECT mr.record_id, mr.patient_id, mr.doctor_id, d.name AS doctor_name,
                       mr.age, mr.gender, mr.symptoms, mr.diagnosis,
                       mr.additional_notes, mr.date
                FROM medical_records mr
                JOIN doctors d ON mr.doctor_id = d.doctor_id
            """
            cursor.execute(query)

        records = cursor.fetchall()
        decrypted_results = []

        for row in records:
            decrypted_row = (
                row[0],                             # record_id
                row[1],                             # patient_id
                row[2],                             # doctor_id
                decrypt_data(row[4]),               # age (encrypted)
                row[5],                             # gender
                decrypt_data(row[6]),               # symptoms (encrypted)
                decrypt_data(row[7]),               # diagnosis (encrypted)
                row[9],                             # date (timestamp)
                decrypt_data(row[3]),               # doctor_name (from JOIN)
                decrypt_data(row[8]) if row[8] else ""  # additional_notes
            )
            decrypted_results.append(decrypted_row)

        cursor.close()
        conn.close()
        return decrypted_results

    except Exception as e:
        print("Error fetching decrypted medical records:", e)
        return []



def get_email_by_username(username, user_type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    table = "patients" if user_type.lower() == "patient" else "doctors"

    try:
        cursor.execute(f"SELECT name, email FROM {table}")
        records = cursor.fetchall()

        for record in records:
            decrypted_name = decrypt_data(record['name'])
            if decrypted_name == username:
                return record['email']

    except Exception as e:
        print(f"Database error while fetching email: {e}")

    finally:
        cursor.close()
        conn.close()

    return None



