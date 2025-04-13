import tkinter as tk
from tkinter import messagebox
from database import Database  # Assuming you have a database.py file
from login import LoginPage  # Assuming you have a login.py file
import bcrypt

class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()
        self.configure(bg="#FFC107")

        tk.Label(self, text="REGISTER", font=("Poppins", 40, "bold"), bg="#FFC107", fg="black").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self, text="First Name", bg="#FFC107", fg="black").grid(row=1, column=0, sticky="w", padx=100)
        self.first_name_entry = tk.Entry(self, bg="white", highlightbackground="gray", highlightthickness=1, borderwidth=0)
        self.first_name_entry.grid(row=1, column=1, pady=5, padx=100, sticky="ew")

        tk.Label(self, text="Last Name", bg="#FFC107", fg="black").grid(row=2, column=0, sticky="w", padx=100)
        self.last_name_entry = tk.Entry(self, bg="white", highlightbackground="gray", highlightthickness=1, borderwidth=0)
        self.last_name_entry.grid(row=2, column=1, pady=5, padx=100, sticky="ew")

        tk.Label(self, text="Email", bg="#FFC107", fg="black").grid(row=3, column=0, sticky="w", padx=100)
        self.email_entry = tk.Entry(self, bg="white", highlightbackground="gray", highlightthickness=1, borderwidth=0)
        self.email_entry.grid(row=3, column=1, pady=5, padx=100, sticky="ew")

        tk.Label(self, text="Phone Number", bg="#FFC107", fg="black").grid(row=4, column=0, sticky="w", padx=100)
        self.phone_entry = tk.Entry(self, bg="white", highlightbackground="gray", highlightthickness=1, borderwidth=0)
        self.phone_entry.grid(row=4, column=1, pady=5, padx=100, sticky="ew")

        tk.Label(self, text="Password", bg="#FFC107", fg="black").grid(row=5, column=0, sticky="w", padx=100)
        self.password_entry = tk.Entry(self, show="*", bg="white", highlightbackground="gray", highlightthickness=1, borderwidth=0)
        self.password_entry.grid(row=5, column=1, pady=5, padx=100, sticky="ew")

        tk.Label(self, text="User Type:", bg="#FFC107", fg="black").grid(row=6, column=0, sticky="w", padx=100)
        self.user_type_var = tk.StringVar(value="Student")
        option_menu = tk.OptionMenu(self, self.user_type_var, "Student", "Faculty", "Visitor")
        option_menu.config(bg="#E0E0E0", relief=tk.RAISED, borderwidth=1, highlightthickness=0)
        option_menu.grid(row=6, column=1, pady=5, padx=100, sticky="ew")

        register_button = tk.Button(self, text="Register", command=self.register, bg="#E0E0E0", relief=tk.RAISED, borderwidth=1)
        register_button.grid(row=7, column=0, columnspan=2, pady=10, padx=50, sticky="ew")

        back_button = tk.Button(self, text="Back to Login", command=lambda: master.switch_page(LoginPage), bg="#E0E0E0", relief=tk.RAISED, borderwidth=1)
        back_button.grid(row=8, column=0, columnspan=2, pady=5, padx=50, sticky="ew")

        self.columnconfigure(1, weight=1)

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

        # Email must contain an '@'
        if '@' not in email or email.startswith('@') or email.endswith('@'):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        # Password must be at least 6 characters
        if len(password) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters long")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            self.db.execute(
                "INSERT INTO Users (UserType, FirstName, LastName, Email, PhoneNumber, Password) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_type, first_name, last_name, email, phone, hashed_password))
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.switch_page(LoginPage)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Register/Login App")
        self.geometry("600x400")
        self.current_page = None
        self.switch_page(LoginPage)

    def switch_page(self, page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self)
        self.current_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()