from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database.db_functions import register_user

def open_register_window(parent_root):
    parent_root.withdraw()
    register_window = Toplevel(parent_root)
    register_window.title("Register")
    register_window.geometry("450x600")
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

    Label(register_window, text="Email:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))
    email_entry = Entry(register_window, font=('Arial', 12), width=32)
    email_entry.pack(pady=5)


    Label(register_window, text="Phone Number:", bg='white', font=('Arial', 12)).pack(pady=(10, 5))

    phone_frame = Frame(register_window, bg='white')
    phone_frame.pack(pady=5)


    country_code_var = StringVar()
    country_code_dropdown = ttk.Combobox(phone_frame, textvariable=country_code_var, state="readonly", width=10, font=('Arial', 11))
    country_code_dropdown['values'] = [
        "PAK(+92)", "USA(+1)", "UK(+44)", "AUS(+61)", "IND(+91)", "UAE(+971)",
        "CAN(+1)", "SA(+966)", "AFG(+93)", "BAN(+880)", "GER(+49)"
    ]

    country_code_dropdown.set("PAK(+92)")  # Default to Pakistan
    country_code_dropdown.pack(side=LEFT, padx=(0, 5))

    phone_entry = Entry(phone_frame, font=('Arial', 12), width=30)
    phone_entry.pack(side=LEFT)

    def validate_and_register():
        import re  # make sure re is imported
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        raw_phone = phone_entry.get().strip()
        selected_country = country_code_dropdown.get()
        user_type = user_type_var.get()
        email = email_entry.get().strip()

        # Extract the country code using regex
        match = re.search(r'\((\+\d+)\)', selected_country)
        if not match:
            messagebox.showerror("Error", f"Invalid country code format: {selected_country}")
            return

        country_code = match.group(1)

        if not username or not password or not raw_phone or not email or user_type == "Select User Type":
            messagebox.showerror("Error", "All fields are required!")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not raw_phone.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits.")
            return

        valid_lengths = {
            "+92": 10, "+1": 10, "+44": 10, "+61": 9, "+91": 10,
            "+971": 9, "+966": 9, "+93": 9, "+880": 10, "+49": 10
        }

        expected_length = valid_lengths.get(country_code)
        if expected_length is None:
            messagebox.showerror("Error", f"Unsupported country code: {country_code}")
            return

        if len(raw_phone) != expected_length:
            messagebox.showerror("Error", f"Phone number for {country_code} must be {expected_length} digits long.")
            return

        phone = f"{country_code}{raw_phone}"

        result = register_user(username, password, phone, email, user_type)

        if result == "exists":
            messagebox.showerror("Error", "User already registered!")
        elif result == "success":
            messagebox.showinfo("Success", "Registration Successful!")
            register_window.destroy()
            parent_root.deiconify()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    Button(register_window, text="Register", bg='#2685f6', fg='white', font=('Arial', 12, 'bold'),
           width=15, command=validate_and_register).pack(pady=55)

    Button(register_window, text="Login", bg='#2685f6', fg='white', font=('Arial', 11, 'bold'),
           border=0, command=lambda: [register_window.destroy(), parent_root.deiconify()]).place(x=15, y=15)



def open_login_window():
    from .login import create_login_frame
    create_login_frame()
