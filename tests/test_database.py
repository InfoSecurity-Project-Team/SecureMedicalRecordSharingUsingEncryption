import pytest
from unittest.mock import patch, MagicMock
from database.db_functions import (
    authenticate_user, register_user,
    get_patient_id_by_name, insert_encrypted_medical_record,
    get_decrypted_medical_records
)

# Sample fake encrypted/decrypted data
ENCRYPTED = lambda x: f"enc({x})"
DECRYPTED = lambda x: x.replace("enc(", "").replace(")", "")


@patch("database.db_functions.get_connection")
@patch("database.db_functions.decrypt_data", side_effect=DECRYPTED)
def test_authenticate_user(mock_decrypt, mock_get_conn):
    # Mock cursor and connection
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{
        'name': ENCRYPTED("alice"),
        'password': ENCRYPTED("password123"),
        'phone': ENCRYPTED("1234567890"),
        'doctor_id': 1
    }]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = authenticate_user("alice", "password123", "doctor")

    assert result['name'] == "alice"
    assert result['phone'] == "1234567890"
    assert result['user_type'] == "doctor"
    assert result['id'] == 1


@patch("database.db_functions.get_connection")
@patch("database.db_functions.encrypt_data", side_effect=ENCRYPTED)
@patch("database.db_functions.decrypt_data", side_effect=DECRYPTED)
def test_register_user_success(mock_decrypt, mock_encrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    # Test user does not exist
    mock_cursor.fetchall.return_value = []
    assert register_user("bob", "pw", "9876543210", "doctor") == "success"

    # Test duplicate username
    mock_cursor.fetchall.return_value = [(ENCRYPTED("bob"),)]
    assert register_user("bob", "pw", "9876543210", "doctor") == "exists"


@patch("database.db_functions.get_connection")
@patch("database.db_functions.decrypt_data", side_effect=DECRYPTED)
def test_get_patient_id_by_name(mock_decrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'patient_id': 42, 'name': ENCRYPTED("charlie")}]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = get_patient_id_by_name("charlie")
    assert result == 42


@patch("database.db_functions.get_connection")
@patch("database.db_functions.encrypt_data", side_effect=ENCRYPTED)
def test_insert_encrypted_medical_record(mock_encrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    success = insert_encrypted_medical_record(
        patient_id=1, doctor_id=2, age=45, gender="Male",
        symptoms=["fever", "cough"], diagnosis="Flu", additional_notes="Rest"
    )
    assert success is True


@patch("database.db_functions.get_connection")
@patch("database.db_functions.decrypt_data", side_effect=DECRYPTED)
def test_get_decrypted_medical_records(mock_decrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, 1, 2, ENCRYPTED("Dr. A"), ENCRYPTED("45"), "Male", ENCRYPTED("fever, cough"),
         ENCRYPTED("Flu"), ENCRYPTED("Notes"), "2024-01-01")
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    records = get_decrypted_medical_records(patient_id=1)
    assert len(records) == 1
    assert records[0][3] == "45"           # age
    assert records[0][5] == "fever, cough" # symptoms
    assert records[0][6] == "Flu"          # diagnosis
    assert records[0][8] == "Dr. A"        # doctor_name
    assert records[0][9] == "Notes"        # additional_notes
