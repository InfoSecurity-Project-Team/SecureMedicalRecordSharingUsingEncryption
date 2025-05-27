import pytest
from unittest.mock import patch, MagicMock
from database import (authenticate_user, register_user, get_patient_id_by_name,
                         insert_encrypted_medical_record, get_decrypted_medical_records)
from crypto import decrypt_data, encrypt_data

# Sample fake encrypted/decrypted data
ENCRYPTED = lambda x: f"enc({x})"
DECRYPTED = lambda x: x.replace("enc(", "").replace(")", "")

@patch("database.get_connection")
@patch("crypto.decrypt_data", side_effect=DECRYPTED)
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


@patch("database.get_connection")
@patch("crypto.encrypt_data", side_effect=ENCRYPTED)
@patch("crypto.decrypt_data", side_effect=DECRYPTED)
def test_register_user_success(mock_decrypt, mock_encrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(ENCRYPTED("bob"),)]
    mock_get_conn.return_value = MagicMock(cursor=MagicMock(return_value=mock_cursor))

    # Test user does not exist
    mock_cursor.fetchall.return_value = []
    assert register_user("bob", "pw", "9876543210", "doctor") == "success"

    # Test duplicate username
    mock_cursor.fetchall.return_value = [(ENCRYPTED("bob"),)]
    assert register_user("bob", "pw", "9876543210", "doctor") == "exists"


@patch("database.get_connection")
@patch("crypto.decrypt_data", side_effect=DECRYPTED)
def test_get_patient_id_by_name(mock_decrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'patient_id': 42, 'name': ENCRYPTED("charlie")}]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    result = get_patient_id_by_name("charlie")
    assert result == 42


@patch("database.get_connection")
@patch("crypto.encrypt_data", side_effect=ENCRYPTED)
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


@patch("database.get_connection")
@patch("crypto.decrypt_data", side_effect=DECRYPTED)
def test_get_decrypted_medical_records(mock_decrypt, mock_get_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, 1, 2, ENCRYPTED("45"), "Male", ENCRYPTED("fever, cough"), ENCRYPTED("Flu"), "2024-01-01", ENCRYPTED("Dr. A"), ENCRYPTED("Notes"))
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    results = get_decrypted_medical_records(patient_id=1)
    assert results[0][3] == "45"  # age
    assert "fever" in results[0][5]
    assert "Flu" in results[0][6]
