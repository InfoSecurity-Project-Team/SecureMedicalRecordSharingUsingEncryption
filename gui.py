from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

root = Tk()
root.title("Medical Records")
root.resizable(False,False)
root.configure(bg='white')
root.geometry('1225x700')


img = Image.open('E:\\coding image\\hospital.jpg')
img = img.resize((550, 550))
img_1 = ImageTk.PhotoImage(img)

d_img = Image.open('E:\\coding image\\hospital.jpg')
d_img = img.resize((550, 550))

l1 = Label(root, image=img_1, background='white')
l1.place(x=50, y=50)
l1.image = img_1

d_img = Image.open('E:\\coding image\\hospital.jpg')
d_img = img.resize((550, 550))
###########################################
# Dashboard
def open_dashboard():
    dashboard = Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    Label(dashboard, text="Welcome to the dashboard!", font=('Arial', 16)).pack(pady=50)
    dashboard.mainloop()
###############################################

    
###############################################
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

p_user = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
p_user.place(x=50, y=120)
add_placeholder(p_user, "Enter username")

p_under_1 = Frame(pat_frame, width=350, height=2, bg='black')
p_under_1.place(x=50, y=140)


p_pass = Text(pat_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
p_pass.place(x=50, y=200)
add_placeholder(p_pass, "Enter password")

p_under_2 = Frame(pat_frame, width=350, height=2, bg='black')
p_under_2.place(x=50, y=220)

def login():
    user = p_user.get("1.0", "end-1c").strip()
    password = p_pass.get("1.0", "end-1c").strip()
    if user == 'ashir' and password == '1234':
        root.destroy()
        open_dashboard()
    else:
        a=messagebox.showerror("Error",'Incorrect credentials written please try again')
        
        


login_button = Button(pat_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
                      cursor='hand2', text='Login', font=('Arial', 10, 'bold'),command=login)
login_button.place(x=195, y=250)



text = Label(pat_frame, text="Don't have an account? ", fg='black', bg='white', font=('Arial', 10, 'bold'))
text.place(x=50, y=380)

signup_button = Button(pat_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
                       cursor='hand2', text='Sign Up', font=('Arial', 10, 'bold'))
signup_button.place(x=210, y=371)
############################################################
#switching to doctor
def switch():
    pat_frame.destroy()

    doc_frame = Frame(root, width=580, height=850, background='white')
    doc_frame.place(x=650, y=70)
    doc_img = Image.open('E:\\coding image\\doc.jpg')
    doc_img = doc_img.resize((200, 200))
    doc_img_tk = ImageTk.PhotoImage(doc_img)

    doc_img_label = Label(doc_frame, image=doc_img_tk, bg='white')
    doc_img_label.image = doc_img_tk
    doc_img_label.place(x=190, y=320)
    Title_2 = Label(doc_frame, text="Doctor Login", fg='#2685f6', bg='white', font=('Helvetica', 23, 'bold'))
    Title_2.place(x=150, y=30)

    d_user = Text(doc_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    d_user.place(x=50, y=120)
    add_placeholder(d_user, "Enter doctor ID")

    d_under_1 = Frame(doc_frame, width=350, height=2, bg='black')
    d_under_1.place(x=50, y=140)

    d_pass = Text(doc_frame, width=38, height=1, fg='black', border=0, bg='white', font=('Arial', 12))
    d_pass.place(x=50, y=200)
    add_placeholder(d_pass, "Enter password")

    d_under_2 = Frame(doc_frame, width=350, height=2, bg='black')
    d_under_2.place(x=50, y=220)

    def doc_login():
        user = d_user.get("1.0", "end-1c").strip()
        password = d_pass.get("1.0", "end-1c").strip()
        if user == 'doctor' and password == 'pass123':
            root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect doctor credentials")

    login_btn = Button(doc_frame, width=12, height=2, border=0, bg='#2685f6', fg='white',
                       cursor='hand2', text='Login', font=('Arial', 10, 'bold'), command=doc_login)
    login_btn.place(x=195, y=250)

    # Doctor Sign Up button
    doc_signup_button = Button(doc_frame, width=7, height=2, border=0, bg='white', fg='#2685f6',
                               cursor='hand2', text='Sign Up', font=('Arial', 10, 'bold'))
    doc_signup_button.place(x=210, y=311)

    # Switch back to Patient frame button
    switch_back_button = Button(doc_frame, width=15, height=2, border=0, bg='white', fg='red',
                                cursor='hand2', text='Switch to Patient', font=('Arial', 10, 'bold'),)
    switch_back_button.place(x=150, y=551)
###################################################################################################

switch_button = Button(pat_frame, width=15, height=2, border=0, bg='white', fg='red',
                       cursor='hand2', text='Switch to Doctor', font=('Arial', 10, 'bold'),command=switch)
switch_button.place(x=400, y=551)



root.mainloop()