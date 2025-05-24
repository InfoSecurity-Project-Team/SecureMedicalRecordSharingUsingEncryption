from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
from database.db_functions import register_user

def open_register_window():
    register_window = Tk()
    register_window.title("Register")
    register_window.geometry("450x500")
    register_window.configure(bg='white')
    register_window.resizable(False, False)

    Label(register_window, text="Registration Window", font=('Arial', 16, 'bold'), fg='#2685f6', bg='white').pack(pady=20)

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
    password_entry = Entry(register_window, font=('Arial', 12), width=32, show="*")
    password_entry.pack(pady=5)

    Label(register_window, text="Phone Number:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))

    phone_frame = Frame(register_window, bg='white')
    phone_frame.pack(pady=5)

    country_code_var = StringVar()
    country_code_dropdown = ttk.Combobox(phone_frame, textvariable=country_code_var, state="readonly", width=6, font=('Arial', 11))
    country_code_dropdown['values'] = ["+92", "+1", "+44", "+61", "+91", "+971"]
    country_code_dropdown.set("+92")  # Default to Pakistan
    country_code_dropdown.pack(side=LEFT, padx=(0, 5))

    phone_entry = Entry(phone_frame, font=('Arial', 12), width=24)
    phone_entry.pack(side=LEFT)


    def validate_and_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        raw_phone = phone_entry.get().strip()
        country_code = country_code_var.get()
        user_type = user_type_var.get()

        phone = f"{country_code}{raw_phone}"

        if not username or not password or not raw_phone or user_type == "Select User Type":
            messagebox.showerror("Error", "All fields are required!")
            return

        if not raw_phone.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits.")
            return

        # Country-specific phone number length validation
        valid_lengths = {
            "+92": 10,  # Pakistan: 10 digits after +92
            "+1": 10,  # USA: 10 digits
            "+44": 10,  # UK (simplified): 10 digits after +44
            "+61": 9,  # Australia: 9 digits
            "+91": 10,  # India: 10 digits
            "+971": 9  # UAE: 9 digits
        }

        expected_length = valid_lengths.get(country_code)

        if expected_length is None:
            messagebox.showerror("Error", f"Unsupported country code: {country_code}")
            return

        if len(raw_phone) != expected_length:
            messagebox.showerror("Error", f"Phone number for {country_code} must be {expected_length+1} digits long.")
            return

        # Register the user
        result = register_user(username, password, phone, user_type)

        if result == "exists":
            messagebox.showerror("Error", "User already registered!")
        elif result == "success":
            messagebox.showinfo("Success", "Registration Successful!")
            register_window.destroy()
            open_login_window()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    Button(register_window, text="Register", bg='#2685f6', fg='white', font=('Arial', 12, 'bold'),
           width=15, command=validate_and_register).pack(pady=15)

    Button(register_window, text="Login", bg='#2685f6', fg='white', font=('Arial', 11, 'bold'),
           border=0, command=lambda: [register_window.destroy(), open_login_window()]).place(x=15, y=15)

    register_window.mainloop()

def open_login_window():
    from .login import create_login_frame
    create_login_frame()
