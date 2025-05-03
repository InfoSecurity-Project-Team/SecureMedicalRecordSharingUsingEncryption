from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

BLUE = "#2685f6"
WHITE = "white"
FONT = ("Segoe UI", 11)

# --- Diagnosis Suggestion Logic ---
def auto_suggest_diagnosis(question_vars):
    answers = {q.lower(): v.get() for q, v in question_vars.items()}

    if (answers.get("fever?", "") == "Yes" and
        answers.get("cough?", "") == "Yes" and
        answers.get("loss of taste or smell?", "") == "Yes" and
        answers.get("fatigue?", "") == "Yes"):
        return "Possible COVID-19"

    elif (answers.get("cough?", "") == "Yes" and
          answers.get("sore throat?", "") == "Yes" and
          answers.get("headache?", "") == "Yes"):
        return "Common Cold"

    elif (answers.get("fever?", "") == "Yes" and
          answers.get("fatigue?", "") == "Yes" and
          answers.get("body aches?", "") == "Yes"):
        return "Influenza (Flu)"

    elif (answers.get("difficulty breathing?", "") == "Yes" and
          answers.get("chest pain?", "") == "Yes"):
        return "Respiratory Infection"

    elif (answers.get("recent travel?", "") == "Yes" and
          (answers.get("fever?", "") == "Yes" or answers.get("cough?", "") == "Yes")):
        return "Travel-related Illness Alert"

    return "General Checkup / No Clear Diagnosis"

# --- Function to Submit the Medical Record ---
def submit_record(name, age, gender, symptoms, diagnosis, doctor_name, notes_func, window):
    if not all([name.get(), age.get(), gender.get(), symptoms.get("1.0", END).strip(),
                diagnosis.get("1.0", END).strip(), doctor_name.get()]):
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

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

    # Diagnosis Questions with Auto-suggestion
    questions = [
        "Fever?", "Cough?", "Loss of Taste or Smell?", "Fatigue?",
        "Sore Throat?", "Headache?", "Body Aches?", "Difficulty Breathing?",
        "Chest Pain?", "Recent Travel?"
    ]

    question_vars = {}

    def update_diagnosis(*args):
        suggestion = auto_suggest_diagnosis(question_vars)
        diagnosis_text.delete("1.0", END)
        diagnosis_text.insert(END, suggestion)

    row_offset = 4
    for idx, question in enumerate(questions):
        Label(form_frame, text=question, font=FONT, bg=WHITE).grid(row=row_offset + idx, column=0, sticky="w", pady=2)
        var = StringVar()
        var.set("No")
        var.trace_add("write", update_diagnosis)
        question_vars[question.lower()] = var
        Radiobutton(form_frame, text="Yes", variable=var, value="Yes", bg=WHITE).grid(row=row_offset + idx, column=1, sticky="w")
        Radiobutton(form_frame, text="No", variable=var, value="No", bg=WHITE).grid(row=row_offset + idx, column=1, sticky="e")

    next_row = row_offset + len(questions)

    form_label("Symptoms:", next_row)
    symptoms_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    symptoms_text.grid(row=next_row, column=1, pady=5)

    form_label("Diagnosis:", next_row + 1)
    diagnosis_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    diagnosis_text.grid(row=next_row + 1, column=1, pady=5)

    form_label("Doctor Name:", next_row + 2)
    doctor_entry = form_entry(next_row + 2)

    form_label("Additional Notes:", next_row + 3)
    notes_text = Text(form_frame, font=FONT, height=3, width=30, bd=1, relief="solid")
    notes_text.grid(row=next_row + 3, column=1, pady=5)

    def compile_notes():
        diagnosis_answers = "\n".join([f"{q} {v.get()}" for q, v in question_vars.items()])
        manual_notes = notes_text.get("1.0", END).strip()
        return f"{diagnosis_answers}\nDoctor Notes: {manual_notes}"

    Button(form_frame, text="Submit Record", bg=BLUE, fg=WHITE,
           font=("Segoe UI", 12, "bold"), width=20,
           command=lambda: submit_record(
               name_entry, age_entry, gender_var, symptoms_text,
               diagnosis_text, doctor_entry, compile_notes, root
           )).grid(row=next_row + 4, column=0, columnspan=2, pady=20)

    root.mainloop()

create_medical_record_gui()
