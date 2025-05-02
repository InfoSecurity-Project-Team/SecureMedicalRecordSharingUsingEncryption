from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

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

def create_patient_login(root, switch_callback, open_dashboard):
    # Load the image only after the root is initialized
    img = Image.open('E:\\coding image\\hospital.jpg')
    img = img.resize((550, 550))
    img_1 = ImageTk.PhotoImage(img)

    pat_frame = Frame(root, width=580, height=850, background='white')
    pat_frame.place(x=650, y=70)

    Title_1 = Label(pat_frame, text="Patient Login", fg='#2685f6', bg='white', font=('Helvetica', 23, 'bold'))
    Title_1.place(x=140, y=30)

    p_user = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    p_user.place(x=50, y=120)
    add_placeholder(p_user, "Enter username")

    Frame(pat_frame, width=350, height=2, bg='black').place(x=50, y=140)

    p_pass = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    p_pass.place(x=50, y=200)
    add_placeholder(p_pass, "Enter password")

    Frame(pat_frame, width=350, height=2, bg='black').place(x=50, y=220)

    def login():
        user = p_user.get("1.0", "end-1c").strip()
        password = p_pass.get("1.0", "end-1c").strip()
        if user == 'ashir' and password == '1234':
            root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", 'Incorrect credentials, please try again')

    Button(pat_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
           cursor='hand2', text='Login', font=('Arial', 10, 'bold'), command=login).place(x=195, y=250)

    Label(pat_frame, text="Don't have an account? ", fg='black', bg='white', font=('Arial', 10, 'bold')).place(x=50, y=380)

    Button(pat_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
           cursor='hand2', text='Sign Up', font=('Arial', 10, 'bold')).place(x=210, y=371)

    Button(pat_frame, width=15, height=2, border=0, bg='white', fg='red',
           cursor='hand2', text='Switch to Doctor', font=('Arial', 10, 'bold'), command=switch_callback).place(x=400, y=551)

    # Return the frame for switching
    return pat_frame
