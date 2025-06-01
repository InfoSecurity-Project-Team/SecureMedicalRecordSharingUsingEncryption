# test_viewMedicalRecord_Module.py

import pytest
from GUI.view_medical_record import search_records_by_patient_id, fetch_all_records
from unittest.mock import patch

def test_search_records_valid_id():
    mock_data = [("1", "P001", "D001", 30, "Male", "Fever", "Flu", "2024-01-01", "Dr. A", "Notes")]
    with patch("GUI.view_medical_record.get_decrypted_medical_records", return_value=mock_data):
        result = search_records_by_patient_id("P001")
        assert result == mock_data

def test_search_records_empty_id():
    with pytest.raises(ValueError):
        search_records_by_patient_id(" ")

def test_fetch_all_records():
    mock_data = [("1", "P001", "D001", 30, "Male", "Fever", "Flu", "2024-01-01", "Dr. A", "Notes")]
    with patch("GUI.view_medical_record.get_decrypted_medical_records", return_value=mock_data):
        result = fetch_all_records()
        assert result == mock_data
