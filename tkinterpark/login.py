import tkinter as tk
from tkinter import messagebox
import bcrypt
from database import Database
from home import HomePage
from PIL import Image, ImageTk

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()
        self.configure(bg="#F4B738")

        # === Container to center content ===
        container = tk.Frame(self, bg="#F4B738")
        container.pack(expand=True, fill="both")

        # === Inner frame to align logo and login form side-by-side ===
        content_frame = tk.Frame(container, bg="#F4B738")
        content_frame.pack(expand=True)

        # === Logo Section ===
        try:
            image = Image.open("Logo.png")
            image = image.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(content_frame, image=photo, bg="#F4B738")
            logo_label.image = photo
            logo_label.pack(side="left", padx=40, pady=20)
        except FileNotFoundError:
            label_text = tk.Label(content_frame, text="LAVA\nCOMB", font=("Poppins", 36, "bold"), bg="#F4B738", fg="white")
            label_text.pack(side="left", padx=40, pady=20)

        # === Login Box ===
        login_frame = tk.Frame(content_frame, bg="white", padx=40, pady=30)
        login_frame.pack(side="left", padx=40, pady=20)

        # === Title ===
        tk.Label(login_frame, text="Login", font=("Arial", 24, "bold"), bg="white", fg="black").pack(pady=(0, 20))

        # === Email ===
        tk.Label(login_frame, text="Email:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.email_entry = tk.Entry(login_frame, bg="lightgray", width=30, relief=tk.FLAT)
        self.email_entry.pack(pady=5)

        # === Password ===
        tk.Label(login_frame, text="Password:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, show="*", bg="lightgray", width=30, relief=tk.FLAT)
        self.password_entry.pack(pady=5)

        # === Buttons ===
        tk.Button(login_frame, text="Login", command=self.login, bg="white", width=12, relief=tk.RAISED, borderwidth=1).pack(pady=(15, 5))
        tk.Button(login_frame, text="Register", command=lambda: master.switch_page(RegisterPage), bg="white", width=12, relief=tk.RAISED, borderwidth=1).pack(pady=(0, 5))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        query = "SELECT UserID, UserType, FirstName, LastName, Email, Password FROM Users WHERE Email = %s"
        user = self.db.fetch_one(query, (email,))

        if user and bcrypt.checkpw(password.encode('utf-8'), user["Password"].encode('utf-8')):
            self.master.show_home(user)
        else:
            messagebox.showerror("Error", "Wrong email or password")

from register import RegisterPage