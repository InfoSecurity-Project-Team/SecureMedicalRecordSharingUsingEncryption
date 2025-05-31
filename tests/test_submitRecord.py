import unittest
from unittest.mock import patch, MagicMock

from GUI.create_medical_record import submit_record  

class TestSubmitRecord(unittest.TestCase):

    def setUp(self):
        # Dummy variables mimicking Tkinter entries and StringVar
        self.name = MagicMock(get=MagicMock(return_value="Ali Hassan"))
        self.age = MagicMock(get=MagicMock(return_value="30"))
        self.gender = MagicMock(get=MagicMock(return_value="Male"))
        self.doctor_name = MagicMock(get=MagicMock(return_value="Dr. Smith"))
        self.doctor_id = MagicMock(get=MagicMock(return_value="D123"))
        self.notes_func = MagicMock(return_value="Feeling unwell.")
        self.window = MagicMock()

        self.symptom_vars = {
            'fever': MagicMock(get=MagicMock(return_value="Yes")),
            'cough': MagicMock(get=MagicMock(return_value="No")),
            'difficulty breathing': MagicMock(get=MagicMock(return_value="No")),
            'fatigue': MagicMock(get=MagicMock(return_value="Yes")),
            'blood pressure': MagicMock(get=MagicMock(return_value="Normal")),
            'cholesterol level': MagicMock(get=MagicMock(return_value="High")),
        }

    @patch("GUI.create_medical_record.get_connection", return_value=None)
    @patch("GUI.create_medical_record.messagebox.showerror")
    def test_db_connection_failure(self, mock_msgbox, mock_conn):
        submit_record(self.name, self.age, self.gender, self.doctor_name,
                      self.doctor_id, self.notes_func, self.window, self.symptom_vars)
        mock_msgbox.assert_called_with("Error", "Database connection failed.")

    @patch("GUI.create_medical_record.get_connection")
    @patch("GUI.create_medical_record.get_patient_id_by_name", return_value=None)
    @patch("GUI.create_medical_record.messagebox.showerror")
    def test_patient_not_found(self, mock_msgbox, mock_get_patient, mock_conn):
        mock_conn.return_value.cursor.return_value = MagicMock()
        submit_record(self.name, self.age, self.gender, self.doctor_name,
                      self.doctor_id, self.notes_func, self.window, self.symptom_vars)
        mock_msgbox.assert_called_with("Error", "Patient not found in the database.")

    @patch("GUI.create_medical_record.get_connection")
    @patch("GUI.create_medical_record.get_patient_id_by_name", return_value=1)
    @patch("GUI.create_medical_record.diagnose", return_value="Flu")
    @patch("GUI.create_medical_record.insert_encrypted_medical_record", return_value=True)
    @patch("GUI.create_medical_record.messagebox.showinfo")
    def test_successful_submission(self, mock_info, mock_insert, mock_diagnose,
                                    mock_get_patient, mock_conn):
        mock_conn.return_value.cursor.return_value = MagicMock()
        submit_record(self.name, self.age, self.gender, self.doctor_name,
                      self.doctor_id, self.notes_func, self.window, self.symptom_vars)
        mock_info.assert_any_call("Diagnosis Result", "Predicted Disease: Flu")
        mock_info.assert_any_call("Success", "Encrypted medical record saved successfully!")

    @patch("GUI.create_medical_record.get_connection")
    @patch("GUI.create_medical_record.get_patient_id_by_name", return_value=1)
    @patch("GUI.create_medical_record.diagnose", side_effect=Exception("Model error"))
    @patch("GUI.create_medical_record.insert_encrypted_medical_record", return_value=True)
    @patch("GUI.create_medical_record.messagebox.showerror")
    def test_diagnosis_failure(self, mock_msgbox, mock_insert, mock_diagnose,
                               mock_get_patient, mock_conn):
        mock_conn.return_value.cursor.return_value = MagicMock()
        submit_record(self.name, self.age, self.gender, self.doctor_name,
                      self.doctor_id, self.notes_func, self.window, self.symptom_vars)
        mock_msgbox.assert_any_call("Diagnosis Failed", "Error while diagnosing: Model error")

if __name__ == '__main__':
    unittest.main()
