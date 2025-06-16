
from tkinter import *
from tkinter import ttk, messagebox
from database.db_connection import get_connection
from database.db_functions import get_decrypted_medical_records

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

# Non-GUI helper functions (testable)
def search_records_by_patient_id(patient_id):
    patient_id = patient_id.strip()
    if not patient_id:
        raise ValueError("Patient ID cannot be empty.")
    return get_decrypted_medical_records(patient_id)

def fetch_all_records():
    return get_decrypted_medical_records()

def view_medical_records_gui(user):
    user_type = user["user_type"]
    doctor_id = user["id"]
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
            records = search_records_by_patient_id(patient_id)  # using helper
            tree.delete(*tree.get_children())
            for record in records:
                tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to search records:\n{e}")

    def view_all_records():
        try:
            records = fetch_all_records()  # using helper
            tree.delete(*tree.get_children())
            for record in records:
                tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch all records:\n{e}")


    Button(search_frame, text="Search", font=FONT, bg=BLUE, fg=WHITE, command=search_records).pack(side=LEFT, padx=10)

    if user_type.lower() == "doctor":
        print("Adding doctor buttons")  # Debug print
        Button(search_frame, text="View All", font=FONT, bg=BLUE, fg=WHITE, command=view_all_records).pack(side=LEFT, padx=5)
        Button(search_frame, text="Create Record", font=FONT, bg=BLUE, fg=WHITE,
            command=lambda: [root.destroy(), create_medical_record_gui(doctor_id)]).pack(side=LEFT, padx=5)

    columns = ("ID", "Patient ID", "Doctor ID", "Age", "Gender", "Symptoms", "Diagnosis", "Visit Date", "Doctor", "Notes")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="w")
    tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

    root.mainloop()

    cursor.close()
    db.close()
