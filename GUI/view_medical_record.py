from tkinter import *
from tkinter import ttk, messagebox  
from db_connection import get_connection  

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

def view_medical_records_gui(user_type):
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

    # Patient ID input
    Label(search_frame, text="Patient ID:", font=FONT, bg=WHITE).pack(side=LEFT, padx=5)
    id_entry = Entry(search_frame, font=FONT, width=30)
    id_entry.pack(side=LEFT, padx=5)

    def search_records():
        patient_id = id_entry.get().strip()
        if not patient_id:
            messagebox.showwarning("Input Error", "Please enter a patient ID to search.")
            return

        try:
            query = "SELECT * FROM medical_records WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            results = cursor.fetchall()
            tree.delete(*tree.get_children())
            for row in results:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to search records:\n{e}")

    def view_all_records():
        cursor.execute("SELECT * FROM medical_records")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", "end", values=row)

    Button(search_frame, text="Search", font=FONT, bg=BLUE, fg=WHITE, command=search_records).pack(side=LEFT, padx=10)

    if user_type == "doctor":
        Button(search_frame, text="View All", font=FONT, bg=BLUE, fg=WHITE, command=view_all_records).pack(side=LEFT, padx=5)

    columns = ("ID", "Patient ID", "Doctor ID", "Age", "Gender", "Symptoms", "Diagnosis", "Visit Date", "Doctor", "Notes")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="w")
    tree.pack(padx=10, pady=10, fill=BOTH, expand=True)

    root.mainloop()

    cursor.close()
    db.close()

if __name__ == "__main__":
    view_medical_records_gui("doctor") 

if __name__ == "__main__":
    view_medical_records_gui("patient")
