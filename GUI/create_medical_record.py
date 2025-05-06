from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from database.db_connection import get_connection
from database.db_functions import get_patient_id_by_name, insert_encrypted_medical_record, get_decrypted_medical_records
from ai_model.model import diagnose

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

def submit_record(name, age, gender, doctor_name, doctor_id_entry, notes_func, window, symptom_vars):
    if not all([name.get(), age.get(), gender.get(), doctor_name.get(), doctor_id_entry.get()]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        cursor = conn.cursor()

        patient_id = get_patient_id_by_name(name.get())
        if not patient_id:
            messagebox.showerror("Error", "Patient not found in the database.")
            return

        # Prepare symptoms list for encryption
        symptom_list = [
            f"Fever: {symptom_vars['fever'].get()}",
            f"Cough: {symptom_vars['cough'].get()}",
            f"Difficult Breathing: {symptom_vars['difficulty breathing'].get()}",
            f"Fatigue: {symptom_vars['fatigue'].get()}",
            f"Blood Pressure: {symptom_vars['blood pressure'].get()}",
            f"Cholesterol Level: {symptom_vars['cholesterol level'].get()}"
        ]

        # Compile diagnosis input for AI model
        diagnosis_input = {
            'Fever': [symptom_vars["fever"].get()],
            'Cough': [symptom_vars["cough"].get()],
            'Fatigue': [symptom_vars["fatigue"].get()] ,
            'Difficulty Breathing': [symptom_vars["difficulty breathing"].get()],
            'Age': [int(age.get())],
            'Gender': [gender.get()],
            'Blood Pressure': [symptom_vars["blood pressure"].get()],
            'Cholesterol Level': [symptom_vars["cholesterol level"].get()]
        }

        # Diagnose the disease
        try:
            disease = diagnose(diagnosis_input)
            messagebox.showinfo("Diagnosis Result", f"Predicted Disease: {disease}")
        except Exception as diag_err:
            messagebox.showerror("Diagnosis Failed", f"Error while diagnosing: {diag_err}")

        # Insert the medical record into the encrypted database
        encrypted_success = insert_encrypted_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id_entry.get(),
            age=age.get(),
            gender=gender.get(),
            symptoms=symptom_list,
            diagnosis=disease,
            additional_notes=notes_func()
        )

        if encrypted_success:
            messagebox.showinfo("Success", "Encrypted medical record saved successfully!")
        else:
            messagebox.showwarning("Warning", "Record saved in diagnosis_records but not encrypted in blockchain.")

        window.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save record: {e}")

def display_records(records):
    # Function to display decrypted records (this could open a new window or update a text box)
    record_window = Toplevel()
    record_window.title("Medical Records")
    
    record_text = Text(record_window, height=20, width=80)
    record_text.pack()
    
    for record in records:
        record_text.insert(END, f"{record}\n")
    
    record_window.mainloop()

def create_medical_record_gui():
    from .view_medical_record import view_medical_records_gui
    root = Tk()
    root.title("Create Medical Record")
    root.geometry('1250x780')
    root.configure(bg=WHITE)
    root.resizable(False, False)

    try:
        img = Image.open("Assets/medform.jpg")
        img = img.resize((500, 500))
        photo = ImageTk.PhotoImage(img)
        image_label = Label(root, image=photo, bg=WHITE)
        image_label.image = photo
        image_label.place(x=50, y=100)
    except Exception as e:
        print("Image failed to load:", e)

    form_frame = Frame(root, bg=WHITE)
    form_frame.place(relx=0.7, rely=0.5, anchor='center')

    Label(form_frame, text="New Record Entry", font=("Segoe UI", 16, "bold"), fg=BLUE, bg=WHITE).grid(row=0, column=0, columnspan=2, pady=10)

    def form_label(text, r):
        return Label(form_frame, text=text, font=FONT, bg=WHITE).grid(row=r, column=0, sticky="w", pady=5)

    def form_entry(r):
        entry = Entry(form_frame, font=FONT, width=30, bd=1, relief="solid")
        entry.grid(row=r, column=1, pady=5)
        return entry

    form_label("Patient Name:", 1)
    name_entry = form_entry(1)

    form_label("Age:", 2)
    age_entry = form_entry(2)

    form_label("Gender:", 3)
    gender_var = StringVar()
    gender_frame = Frame(form_frame, bg=WHITE)
    gender_frame.grid(row=3, column=1, pady=5, sticky="w")
    Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", font=FONT, bg=WHITE).pack(side=LEFT)
    Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", font=FONT, bg=WHITE).pack(side=LEFT)

    symptom_questions = {
        "fever": ["Yes", "No"],
        "cough": ["Yes", "No"],
        "difficulty breathing": ["Yes", "No"],
        "fatigue": ["Yes", "No"],
        "blood pressure": ["Low", "Normal", "High"],
        "cholesterol level": ["Low", "Normal", "High"]
    }

    symptom_vars = {}
    row_offset = 4

    for i, (symptom, options) in enumerate(symptom_questions.items()):
        form_label(symptom.replace('_', ' ').title() + ":", row_offset + i)
        var = StringVar(value=options[0])
        symptom_vars[symptom] = var
        frame = Frame(form_frame, bg=WHITE)
        frame.grid(row=row_offset + i, column=1, sticky="w")
        for opt in options:
            Radiobutton(frame, text=opt, variable=var, value=opt, bg=WHITE).pack(side=LEFT)

    next_row = row_offset + len(symptom_questions)

    form_label("Doctor Name:", next_row)
    doctor_entry = form_entry(next_row)

    form_label("Doctor ID:", next_row + 1)
    doctor_id_entry = form_entry(next_row + 1)

    form_label("Additional Notes:", next_row + 2)
    notes_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    notes_text.grid(row=next_row + 2, column=1, pady=5)

    def compile_notes():
        return notes_text.get("1.0", END).strip()

    Button(form_frame, text="Submit Record", bg=BLUE, fg=WHITE,
           font=("Segoe UI", 12, "bold"), width=20,
           command=lambda: submit_record(
               name_entry, age_entry, gender_var,
               doctor_entry, doctor_id_entry, compile_notes, root, symptom_vars
           )).grid(row=next_row + 3, column=0, columnspan=2, pady=20)

    Button(form_frame, text="View Records", bg=BLUE, fg=WHITE,
       font=("Segoe UI", 12, "bold"), width=20,
       command=view_medical_records_gui
       ).grid(row=next_row + 4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    create_medical_record_gui()
