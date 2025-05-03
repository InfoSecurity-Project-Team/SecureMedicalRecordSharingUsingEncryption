from tkinter import *
from tkinter import ttk

def open_register_window():
    register_window = Tk()  
    register_window.title("Register")
    register_window.geometry("400x500")
    register_window.configure(bg='white')

    Label(register_window, text="Registration Window", font=('Arial', 16,'bold'), fg='#2685f6',bg='white').pack(pady=20)

    Label(register_window, text="User Type:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    user_type_var = StringVar()
    user_type_dropdown = ttk.Combobox(register_window, textvariable=user_type_var, state="readonly",
                                      values=["Doctor", "Patient"], font=('Arial', 12), width=30)
    user_type_dropdown.set("Select User Type")
    user_type_dropdown.pack(pady=5)

    Label(register_window, text="Username:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    username_entry = Entry(register_window, font=('Arial', 12), width=32)
    username_entry.pack(pady=5)

    Label(register_window, text="Password:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    password_entry = Entry(register_window, font=('Arial', 12), width=32)
    password_entry.pack(pady=5)

    Label(register_window, text="Address:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    address_entry = Entry(register_window, font=('Arial', 12), width=32)
    address_entry.pack(pady=5)

    Label(register_window, text="Phone Number:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    phone_entry = Entry(register_window, font=('Arial', 12), width=32)
    phone_entry.pack(pady=5)

    Button(register_window, text="Register", bg='#2685f6', fg='white', font=('Arial', 12, 'bold'),
           width=15, command=lambda: print("Register logic here")).pack(pady=15)

    Button(register_window, text="Close", bg='white', fg='#2685f6', font=('Arial', 11, 'bold'),
           border=0, command=register_window.destroy).pack(pady=5)

    register_window.mainloop()
