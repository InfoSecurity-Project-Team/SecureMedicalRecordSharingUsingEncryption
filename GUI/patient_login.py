from tkinter import *
from tkinter import messagebox

def create_patient_login(root, on_login_success, on_register_click):
    pat_frame = Frame(root, width=580, height=850, background='white')
    pat_frame.place(x=650, y=70)

    Title_1 = Label(pat_frame, text="Patient Login", fg='#2685f6', bg='white', font=('Helvetica', 23, 'bold'))
    Title_1.place(x=140, y=30)

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

    user = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    user.place(x=50, y=120)
    add_placeholder(user, "Doctor/Patient")

    p_under = Frame(pat_frame, width=350, height=2, bg='black')
    p_under.place(x=50, y=140)

    p_user = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    p_user.place(x=50, y=180)
    add_placeholder(p_user, "Enter username")

    p_under_1 = Frame(pat_frame, width=350, height=2, bg='black')
    p_under_1.place(x=50, y=200)

    p_pass = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    p_pass.place(x=50, y=240)
    add_placeholder(p_pass, "Enter password")

    p_under_2 = Frame(pat_frame, width=350, height=2, bg='black')
    p_under_2.place(x=50, y=260)

    def login():
        username = p_user.get("1.0", "end-1c").strip()
        password = p_pass.get("1.0", "end-1c").strip()
        if username == 'ashir' and password == '1234':
            root.destroy()
            on_login_success()
        else:
            messagebox.showerror("Error", 'Incorrect credentials written, please try again')

    login_button = Button(pat_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
                          cursor='hand2', text='Login', font=('Arial', 10, 'bold'), command=login)
    login_button.place(x=195, y=300)

    text = Label(pat_frame, text="Don't have an account? ", fg='black', bg='white', font=('Arial', 10, 'bold'))
    text.place(x=50, y=410)

    signup_button = Button(pat_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
                           cursor='hand2', text='Register', font=('Arial', 10, 'bold'),
                           command=on_register_click)
    signup_button.place(x=210, y=401)
