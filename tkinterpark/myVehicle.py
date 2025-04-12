import tkinter as tk
from database import Database

class MyVehiclesPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        self.configure(bg="#F4B738")  # Orange background

        # Navigation Buttons (Top)
        button_frame = tk.Frame(self, bg='#F4B738')
        button_frame.pack(fill=tk.X, pady=30, padx=30)

        button_width = 18
        button_height = 2
        button_font = ("Poppins", 10, "bold")
        button_bg = "#FFFFFF"
        button_bd = 3
        button_relief = "raised"

        tk.Button(button_frame, text="HOME", command=lambda: self.master.show_home(self.user), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="AVAILABLE SLOTS", command=master.show_available_slots, width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="REGISTER VEHICLE", command=lambda: self.master.show_register_vehicle(), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="PARKING HISTORY", command=lambda: self.master.show_parking_history(),
                  width=button_width, height=button_height, font=button_font, bg=button_bg, bd=button_bd,
                  relief=button_relief).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="LOGOUT", command=lambda: self.master.show_login(), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.RIGHT, padx=10, pady=10)

        # Title Label
        tk.Label(self, text="YOUR VEHICLE", font=("Poppins", 24, "bold"), bg="#F4B738").pack(pady=25)

        # Unified Table Section
        table_frame = tk.Frame(self, bg="#E5E4E2")
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        headers = ["Type", "License Plate", "Make", "Model", "Color"]
        header_frame = tk.Frame(table_frame, bg="#E5E4E2")
        header_frame.pack(fill=tk.X)

        for col, text in enumerate(headers):
            tk.Label(header_frame, text=text, font=("Poppins", 11), padx=10, pady=8,
                     bg="#E5E4E2", fg="black", borderwidth=1, relief="solid", anchor="center").grid(
                row=0, column=col, sticky="nsew")
            header_frame.grid_columnconfigure(col, weight=1)

        # Vehicle List Frame
        self.vehicles_frame = tk.Frame(table_frame, bg="white", bd=1, relief="solid")
        self.vehicles_frame.pack(fill=tk.BOTH, expand=True)

        self.load_vehicles()

    def load_vehicles(self):
        # Clear previous data
        for widget in self.vehicles_frame.winfo_children():
            widget.destroy()

        query = "SELECT VehicleType, LicensePlate, Make, Model, Color FROM Vehicles WHERE UserID = %s"
        vehicles = self.db.fetch_all(query, (self.user["UserID"],))

        if not vehicles:
            tk.Label(self.vehicles_frame, text="No vehicles found.", font=("Poppins", 12), bg="white", pady=10).pack()
        else:
            for row_idx, vehicle in enumerate(vehicles):
                row_color = "#FFFFFF" if row_idx % 2 == 0 else "#F5F5F5"  # Alternating row colors
                for col_idx, key in enumerate(["VehicleType", "LicensePlate", "Make", "Model", "Color"]):
                    tk.Label(self.vehicles_frame, text=vehicle[key], padx=10, pady=5,
                             bg=row_color, font=("Poppins", 10), anchor="center").grid(
                        row=row_idx, column=col_idx, sticky="nsew")
                    self.vehicles_frame.grid_columnconfigure(col_idx, weight=1)
