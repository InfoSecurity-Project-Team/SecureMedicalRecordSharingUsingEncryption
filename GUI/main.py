from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from patient_login import create_patient_login
from doctor_login import create_doctor_login

def open_dashboard():
    dashboard = Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    Label(dashboard, text="Welcome to the dashboard!", font=('Arial', 16)).pack(pady=50)
    dashboard.mainloop()

root = Tk()
root.title("Medical Records")
root.geometry('1225x700')
root.configure(bg='white')
root.resizable(False, False)

def load_images():
    hospital_img = Image.open('Assets/hospital.jpg').resize((550, 550))
    hospital_img_tk = ImageTk.PhotoImage(hospital_img)

    doctor_img = Image.open('Assets/doc.jpg').resize((550, 550))
    doctor_img_tk = ImageTk.PhotoImage(doctor_img)
    
    return hospital_img_tk, doctor_img_tk

hospital_img_tk, doctor_img_tk = load_images()

image_label = Label(root, bg='white')
image_label.place(x=50, y=50)

current_frame = None

# Define switch_to_doctor function
def switch_to_doctor():
    global current_frame
    if current_frame:
        current_frame.destroy()
    image_label.configure(image=doctor_img_tk)
    image_label.image = doctor_img_tk
    current_frame = create_doctor_login(root, switch_to_patient, open_dashboard)

# Define switch_to_patient function
def switch_to_patient():
    global current_frame
    if current_frame:
        current_frame.destroy()
    image_label.configure(image=hospital_img_tk)
    image_label.image = hospital_img_tk
    current_frame = create_patient_login(root, switch_to_doctor, open_dashboard)

# Start with patient login
switch_to_patient()

root.mainloop()
