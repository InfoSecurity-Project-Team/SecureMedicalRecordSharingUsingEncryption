from tkinter import *
from tkinter import ttk, messagebox

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

def view_medical_records_gui(user_type):
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
        # 🔍 Dummy example - clear then insert mock data
        tree.delete(*tree.get_children())
        tree.insert("", "end", values=("001", patient_name, "25", "Male", "Fever", "Flu", "2025-04-01", "Dr. Khan", "Rest & fluids"))

    def view_all_records():
        # 📋 Dummy example - insert some mock data
        tree.delete(*tree.get_children())
        sample_data = [
            ("001", "Ali", "25", "Male", "Fever", "Flu", "2025-04-01", "Dr. Khan", "Rest & fluids"),
            ("002", "Sara", "30", "Female", "Cough", "Cold", "2025-04-02", "Dr. Ali", "Cough syrup")
        ]
        for record in sample_data:
            tree.insert("", "end", values=record)

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

# --- Call the GUI function based on user role ---
# Example:
view_medical_records_gui("patient")
view_medical_records_gui("doctor")
