from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from patient_login import create_patient_login
from register_window import open_register_window  

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



    return hospital_img_tk

hospital_img_tk = load_images()

image_label = Label(root, image=hospital_img_tk, bg='white')
image_label.place(x=50, y=50)
image_label.image = hospital_img_tk  # keep reference

create_patient_login(root, open_dashboard, open_register_window)  

root.mainloop()
