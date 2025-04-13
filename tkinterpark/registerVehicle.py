import tkinter as tk
from tkinter import messagebox
from database import Database


class RegisterVehiclePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        self.configure(bg="#F4B738")  # Match background color from the image

        tk.Label(self, text="REGISTER VEHICLE", font=("Poppins", 28, "bold"), bg="#F4B738", fg="black").pack(pady=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg="#f4b630")
        nav_frame.pack(pady=10)

        button_style = {"width": 18, "height": 2, "bg": "white", "fg": "black", "font": ("Arial", 10, "bold"),
                        "relief": "raised", "bd": 3}
        tk.Button(nav_frame, text="HOME", command=lambda: master.show_home(master.user), **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="AVAILABLE SLOTS", command=master.show_available_slots, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="MY VEHICLES", command=master.show_my_vehicles, **button_style).pack(side=tk.LEFT,padx=5)
        tk.Button(nav_frame, text="PARKING HISTORY", command=master.show_parking_history, **button_style).pack(side=tk.LEFT,padx=5)
        tk.Button(nav_frame, text="LOGOUT", command=master.show_login, **button_style).pack(side=tk.LEFT, padx=5)

        # Form fields
        form_frame = tk.Frame(self, bg="#f4b630")
        form_frame.pack(pady=30)

        label_font = ("Poppins", 12, "bold")
        entry_font = ("Poppins", 10, "bold")

        # Vehicle Type
        tk.Label(form_frame, text="Vehicle Type:", font=label_font, bg="#f4b630").pack(pady=(5, 0))
        self.vehicle_type_var = tk.StringVar(value="Car")
        vehicle_type_menu = tk.OptionMenu(form_frame, self.vehicle_type_var, "Car", "Motorcycle")
        vehicle_type_menu.config(font=entry_font, width=20)
        vehicle_type_menu.pack(pady=(0, 10))

        # License Plate
        tk.Label(form_frame, text="License Plate:", font=label_font, bg="#f4b630").pack(pady=(5, 0))
        self.license_plate_entry = tk.Entry(form_frame, font=entry_font, justify="center", width=25)
        self.license_plate_entry.pack(pady=(0, 10))

        # Made By
        tk.Label(form_frame, text="Made By:", font=label_font, bg="#f4b630").pack(pady=(5, 0))
        self.make_entry = tk.Entry(form_frame, font=entry_font, justify="center", width=25)
        self.make_entry.pack(pady=(0, 10))

        # Model
        tk.Label(form_frame, text="Model:", font=label_font, bg="#f4b630").pack(pady=(5, 0))
        self.model_entry = tk.Entry(form_frame, font=entry_font, justify="center", width=25)
        self.model_entry.pack(pady=(0, 10))

        # Color
        tk.Label(form_frame, text="Color:", font=label_font, bg="#f4b630").pack(pady=(5, 0))
        self.color_entry = tk.Entry(form_frame, font=entry_font, justify="center", width=25)
        self.color_entry.pack(pady=(0, 15))

        # Submit Button
        tk.Button(self, text="REGISTER VEHICLE", font=entry_font, width=20, height=2, bg="white", fg="black",
                  relief="raised", bd=4,
                  command=self.register_vehicle).pack()

    def register_vehicle(self):
        """Registers a vehicle for the logged-in user"""
        vehicle_type = self.vehicle_type_var.get()
        license_plate = self.license_plate_entry.get().strip()
        make = self.make_entry.get().strip()
        model = self.model_entry.get().strip()
        color = self.color_entry.get().strip()

        if not (vehicle_type and license_plate and make and model and color):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check if license plate already exists
        query = "SELECT * FROM Vehicles WHERE LicensePlate = %s"
        existing_vehicle = self.db.fetch_one(query, (license_plate,))
        if existing_vehicle:
            messagebox.showerror("Error", "License plate already registered!")
            return

        # Insert into database
        insert_query = """
            INSERT INTO Vehicles (UserID, VehicleType, LicensePlate, Make, Model, Color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute(insert_query, (self.user["UserID"], vehicle_type, license_plate, make, model, color))

        messagebox.showinfo("Success", "Vehicle registered successfully!")
        self.master.show_my_vehicles()  # Redirect to My Vehicles page after registration