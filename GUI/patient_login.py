from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
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

hospital_img = Image.open('Assets/hospital.jpg').resize((550, 550))
hospital_img_tk = ImageTk.PhotoImage(hospital_img)

image_label = Label(root, image=hospital_img_tk, bg='white')
image_label.place(x=50, y=50)
image_label.image = hospital_img_tk

def add_placeholder(widget, placeholder):
    def on_focus_in(event):
        if widget.get("1.0", "end-1c") == placeholder:
            widget.delete("1.0", "end")
            widget.config(fg='black')

    def on_focus_out(event):
        if widget.get("1.0", "end-1c").strip() == "":
            widget.insert("1.0", placeholder)
            widget.config(fg='grey')

    widget.insert("1.0", placeholder)
    widget.config(fg='grey')
    widget.bind("<FocusIn>", on_focus_in)
    widget.bind("<FocusOut>", on_focus_out)

def create_login_frame():
    global username, password

    pat_frame = Frame(root, width=580, height=850, background='white')
    pat_frame.place(x=650, y=70)

    Title_1 = Label(pat_frame, text="Login", fg='#2685f6', bg='white', font=('Helvetica', 23, 'bold'))
    Title_1.place(x=200, y=30)

    user_type_var = StringVar(value="Select User Type")
    user_type_dropdown = ttk.Combobox(pat_frame, textvariable=user_type_var, state="readonly",
                                    values=["Doctor", "Patient"], font=('Arial', 12), width=36)
    user_type_dropdown.place(x=50, y=120)

    def on_select(event):
        if user_type_var.get() == "Select User Type":
            user_type_var.set("") 

    user_type_dropdown.bind('<<ComboboxSelected>>', on_select)

    username = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    username.place(x=50, y=180)
    add_placeholder(username, "Enter username")
    Frame(pat_frame, width=350, height=2, bg='black').place(x=50, y=200)

    password = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    password.place(x=50, y=240)
    add_placeholder(password, "Enter password")
    Frame(pat_frame, width=350, height=2, bg='black').place(x=50, y=260)

    def login():
        entered_user = username.get("1.0", "end-1c").strip()
        entered_pass = password.get("1.0", "end-1c").strip()
        if entered_user == 'ashir' and entered_pass == '1234':
            root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect credentials written please try again")

    Button(pat_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
           cursor='hand2', text='Login', font=('Arial', 10, 'bold'), command=login).place(x=195, y=300)

    Label(pat_frame, text="Don't have an account? ", fg='black', bg='white', font=('Arial', 10, 'bold')).place(x=50, y=410)

    Button(pat_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
           cursor='hand2', text='Register', font=('Arial', 10, 'bold'), command=lambda: [root.destroy(), open_register_window()]).place(x=210, y=401)

create_login_frame()
root.mainloop()
