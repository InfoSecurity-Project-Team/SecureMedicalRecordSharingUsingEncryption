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

    Label(search_frame, text="Patient Name:", font=FONT, bg=WHITE).pack(side=LEFT, padx=5)
    name_entry = Entry(search_frame, font=FONT, width=30)
    name_entry.pack(side=LEFT, padx=5)

    def search_records():
        patient_name = name_entry.get().strip()
        if not patient_name:
            messagebox.showwarning("Input Error", "Please enter a patient name to search.")
            return

        query = "SELECT * FROM records WHERE name LIKE %s"
        cursor.execute(query, (f"%{patient_name}%",))
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", "end", values=row)

    def view_all_records():
        cursor.execute("SELECT * FROM records")
        results = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in results:
            tree.insert("", "end", values=row)

    Button(search_frame, text="Search", font=FONT, bg=BLUE, fg=WHITE, command=search_records).pack(side=LEFT, padx=10)

    if user_type == "doctor":
        Button(search_frame, text="View All", font=FONT, bg=BLUE, fg=WHITE, command=view_all_records).pack(side=LEFT, padx=5)

    columns = ("ID", "Name", "Age", "Gender", "Symptoms", "Diagnosis", "Visit Date", "Doctor", "Notes")
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
