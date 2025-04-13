import tkinter as tk
from tkinter import messagebox
from database import Database
from login import LoginPage
import bcrypt

class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F4B738")
        self.db = Database()

        # Allow resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Canvas for rounded-style background
        canvas = tk.Canvas(self, bg="#F4B738", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Frame that holds content
        self.content = tk.Frame(canvas, bg="#F4B738")

        # Function to resize and center content
        def resize_content(event):
            width = event.width
            height = event.height
            canvas.delete("all")
            canvas.create_rectangle(50, 20, width - 50, height - 15, outline="", fill="#F4B738", width=0)
            canvas.create_window(width // 2, height // 2, window=self.content, anchor="center")

        canvas.bind("<Configure>", resize_content)

        # Title
        tk.Label(self.content, text="REGISTER", font=("Poppins", 24, "bold"),
                 bg="#F4B738", fg="black").grid(row=0, column=0, columnspan=2, pady=(2,2))

        # Helpers
        def create_label(row, text):
            tk.Label(self.content, text=text + ":", font=("Poppins", 12),
                     bg="#F4B738", anchor="w").grid(row=row, column=0, sticky="e",
                                                    padx=(10, 5), pady=6)

        def create_entry(row, show=None):
            entry = tk.Entry(self.content, font=("Poppins", 11), bg="white",
                             relief="flat", show=show)
            entry.grid(row=row, column=1, padx=(0, 10), pady=6, ipady=3, sticky="ew")
            return entry

        self.content.grid_columnconfigure(1, weight=1)

        # Fields
        create_label(1, "First Name")
        self.first_name_entry = create_entry(1)

        create_label(2, "Last Name")
        self.last_name_entry = create_entry(2)

        create_label(3, "Email")
        self.email_entry = create_entry(3)

        create_label(4, "Phone Number")
        self.phone_entry = create_entry(4)

        create_label(5, "Password")
        self.password_entry = create_entry(5, show="*")

        create_label(6, "User Type")
        self.user_type_var = tk.StringVar(value="Student")
        dropdown = tk.OptionMenu(self.content, self.user_type_var, "Student", "Faculty", "Visitor")
        dropdown.config(font=("Poppins", 11), bg="white", relief="flat",
                        highlightthickness=1, bd=1)
        dropdown.grid(row=6, column=1, sticky="ew", padx=(0, 10), pady=6)

        # Register Button
        register_btn = tk.Button(self.content, text="Register", command=self.register,
                                 font=("Poppins", 11, "bold"), bg="#E0E0E0", relief="flat")
        register_btn.grid(row=7, column=0, columnspan=2, pady=(20, 10),
                          ipadx=10, ipady=5, sticky="ew", padx=40)

        # Back to Login Button
        back_btn = tk.Button(self.content, text="Back to Login",
                             command=lambda: master.switch_page(LoginPage),
                             font=("Poppins", 11, "bold"), bg="#E0E0E0", relief="flat")
        back_btn.grid(row=8, column=0, columnspan=2, pady=(5, 20),
                      ipadx=10, ipady=5, sticky="ew", padx=40)

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if not (first_name and last_name and email and password):
            messagebox.showerror("Error", "All fields are required!")
            return

        if '@' not in email or email.startswith('@') or email.endswith('@'):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        if len(password) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters long")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            self.db.execute(
                "INSERT INTO Users (UserType, FirstName, LastName, Email, PhoneNumber, Password) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (user_type, first_name, last_name, email, phone, hashed_password))
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.switch_page(LoginPage)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
