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

def create_doctor_login(root, switch_callback, open_dashboard):
    doc_frame = Frame(root, width=580, height=850, background='white')
    doc_frame.place(x=650, y=70)

    Title_2 = Label(doc_frame, text="Doctor Login", fg='#2685f6', bg='white', font=('Helvetica', 23, 'bold'))
    Title_2.place(x=150, y=30)

    d_user = Text(doc_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    d_user.place(x=50, y=120)
    add_placeholder(d_user, "Enter username")

    Frame(doc_frame, width=350, height=2, bg='black').place(x=50, y=140)

    d_pass = Text(doc_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    d_pass.place(x=50, y=200)
    add_placeholder(d_pass, "Enter password")

    Frame(doc_frame, width=350, height=2, bg='black').place(x=50, y=220)

    def doc_login():
        user = d_user.get("1.0", "end-1c").strip()
        password = d_pass.get("1.0", "end-1c").strip()
        if user == 'doctor' and password == 'pass123':
            root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect doctor credentials")

    Button(doc_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
           cursor='hand2', text='Login', font=('Arial', 10, 'bold'), command=doc_login).place(x=195, y=250)

    Button(doc_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
           cursor='hand2', text='Sign Up', font=('Arial', 10, 'bold')).place(x=210, y=371)

    Label(doc_frame, text="Don't have an account? ", fg='black', bg='white', font=('Arial', 10, 'bold')).place(x=50, y=380)

    Button(doc_frame, width=15, height=2, border=0, bg='white', fg='red',
           cursor='hand2', text='Switch to Patient', font=('Arial', 10, 'bold'), command=switch_callback).place(x=400, y=551)

    root.update()  

    return doc_frame
