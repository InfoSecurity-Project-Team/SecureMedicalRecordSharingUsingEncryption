from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from db_connection import get_connection  

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

def submit_record(name, age, gender, symptoms, doctor_name, notes_func, window, symptom_vars):
    if not all([name.get(), age.get(), gender.get(), symptoms.get("1.0", END).strip(), doctor_name.get()]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        cursor = conn.cursor()


        query = """
            INSERT INTO diagnosis_records (
                name, age, gender, symptoms_description, doctor_name, notes,
                fever, cough, difficulty_breathing, fatigue,
                blood_pressure, cholesterol_level, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            name.get(),
            int(age.get()),
            gender.get(),
            symptoms.get("1.0", END).strip(),
            doctor_name.get(),
            notes_func(),
            symptom_vars["fever"].get(),
            symptom_vars["cough"].get(),
            symptom_vars["difficulty breathing"].get(),
            symptom_vars["fatigue"].get(),
            symptom_vars["blood pressure"].get(),
            symptom_vars["cholesterol level"].get(),
            datetime.datetime.now()
        )

        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Medical record saved to database successfully!")
        window.destroy() 
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save record: {e}")

def create_medical_record_gui():
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

    # --- Symptom Inputs ---
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

    form_label("Symptoms:", next_row)
    symptoms_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    symptoms_text.grid(row=next_row, column=1, pady=5)

    form_label("Doctor Name:", next_row + 1)
    doctor_entry = form_entry(next_row + 1)

    form_label("Additional Notes:", next_row + 2)
    notes_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    notes_text.grid(row=next_row + 2, column=1, pady=5)

    def compile_notes():
        return notes_text.get("1.0", END).strip()

    Button(form_frame, text="Submit Record", bg=BLUE, fg=WHITE,
           font=("Segoe UI", 12, "bold"), width=20,
           command=lambda: submit_record(
               name_entry, age_entry, gender_var, symptoms_text,
               doctor_entry, compile_notes, root, symptom_vars
           )).grid(row=next_row + 3, column=0, columnspan=2, pady=20)

    root.mainloop()

create_medical_record_gui()
