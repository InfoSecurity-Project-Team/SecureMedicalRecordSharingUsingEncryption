from tkinter import *
from tkinter import ttk, messagebox
from database.db_connection import get_connection
from database.db_functions import get_patient_id_by_name, insert_encrypted_medical_record, get_decrypted_medical_records

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

def view_medical_records_gui(user_type="doctor"):
    from .create_medical_record import create_medical_record_gui
    try:
        db = get_connection()
        cursor = db.cursor()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
        return

    root = Tk()
    root.title("View Medical Records")
    root.geometry("1100x600")
    root.configure(bg=WHITE)
    root.resizable(False, False)

    Label(root, text="Medical Records Viewer", font=("Segoe UI", 16, "bold"), fg=BLUE, bg=WHITE).pack(pady=10)

    search_frame = Frame(root, bg=WHITE)
    search_frame.pack(pady=10)

    Label(search_frame, text="Patient ID:", font=FONT, bg=WHITE).pack(side=LEFT, padx=5)
    id_entry = Entry(search_frame, font=FONT, width=30)
    id_entry.pack(side=LEFT, padx=5)

    def search_records():
        patient_id = id_entry.get().strip()
        if not patient_id:
            messagebox.showwarning("Input Error", "Please enter a patient ID to search.")
            return

        try:
            # Fetch encrypted records based on patient_id
            records = get_decrypted_medical_records(patient_id)
            tree.delete(*tree.get_children())
            for record in records:
                tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to search records:\n{e}")

    def view_all_records():
        try:
            # Fetch all encrypted records if no patient_id is provided
            records = get_decrypted_medical_records()
            tree.delete(*tree.get_children())
            for record in records:
                tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch all records:\n{e}")

    Button(search_frame, text="Search", font=FONT, bg=BLUE, fg=WHITE, command=search_records).pack(side=LEFT, padx=10)

    if user_type == "doctor":
        Button(search_frame, text="View All", font=FONT, bg=BLUE, fg=WHITE, command=view_all_records).pack(side=LEFT, padx=5)

        Button(root, text="Back to Create Record", font=FONT, bg=BLUE, fg=WHITE, command=lambda: [root.destroy(), create_medical_record_gui()]).pack(pady=20)

    columns = ("ID", "Patient ID", "Doctor ID", "Age", "Gender", "Symptoms", "Diagnosis", "Visit Date", "Doctor", "Notes")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="w")
    tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

    root.mainloop()

    cursor.close()
    db.close()

def insert_medical_record(patient_id, doctor_id, age, gender, symptoms, diagnosis, visit_date, doctor, notes):
    try:
        # Convert symptoms to list format if it's a string
        if isinstance(symptoms, str):
            symptoms = symptoms.split(',')  # Split string into list
        
        # Insert encrypted record with Symptoms as a list
        insert_encrypted_medical_record(patient_id, doctor_id, age, gender, symptoms, diagnosis, visit_date, doctor, notes)
        messagebox.showinfo("Success", "Medical record inserted successfully.")
    except Exception as e:
        messagebox.showerror("Insert Error", f"Failed to insert record:\n{e}")

if __name__ == "__main__":
    view_medical_records_gui("doctor")

    view_medical_records_gui("patient")
