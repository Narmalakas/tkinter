import tkinter as tk
from database import Database

class MyVehiclesPage(tk.Frame):
    def __init__(self, master, user):
        master.geometry("850x500")
        master.update_idletasks()

        super().__init__(master, width=850, height=500)
        self.pack_propagate(False)

        self.master = master
        self.user = user
        self.db = Database()

        self.configure(bg="#F4B738")

        # Title
        tk.Label(self, text="YOUR VEHICLE", font=("Poppins", 24, "bold"), bg="#F4B738").pack(pady=(20, 5))

        # Navigation Buttons
        button_frame = tk.Frame(self, bg="#F4B738")
        button_frame.pack(fill=tk.X, pady=10, padx=30)

        button_settings = {
            "width": 18,
            "height": 2,
            "font": ("Poppins", 10, "bold"),
            "bg": "#FFFFFF",
            "bd": 3,
            "relief": "raised",
        }

        tk.Button(button_frame, text="HOME", command=lambda: self.master.show_home(self.user), **button_settings).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="AVAILABLE SLOTS", command=self.master.show_available_slots, **button_settings).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="REGISTER VEHICLE", command=self.master.show_register_vehicle, **button_settings).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="PARKING HISTORY", command=self.master.show_parking_history, **button_settings).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="LOGOUT", command=self.master.show_login, **button_settings).pack(side=tk.RIGHT, padx=10, pady=10)

        # Combined Table Frame
        self.table_frame = tk.Frame(self, bg="#E5E4E2")
        self.table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Load vehicles and build the table
        self.load_vehicles()

    def load_vehicles(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["Type", "License Plate", "Make", "Model", "Color"]
        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame,
                text=header,
                font=("Poppins", 11, "bold"),
                bg="#DCDCDC",
                fg="black",
                padx=10,
                pady=8,
                borderwidth=1,
                relief="solid",
                anchor="center"
            ).grid(row=0, column=col, sticky="nsew", ipadx=5, ipady=5)
            self.table_frame.grid_columnconfigure(col, weight=1)

        query = "SELECT VehicleType, LicensePlate, Make, Model, Color FROM Vehicles WHERE UserID = %s"
        vehicles = self.db.fetch_all(query, (self.user["UserID"],))

        if not vehicles:
            tk.Label(self.table_frame, text="No vehicles found.", font=("Poppins", 12), bg="white", pady=10).grid(
                row=1, column=0, columnspan=5, sticky="nsew"
            )
        else:
            for row_idx, vehicle in enumerate(vehicles, start=1):
                row_color = "#FFFFFF" if row_idx % 2 == 1 else "#F5F5F5"
                for col_idx, key in enumerate(["VehicleType", "LicensePlate", "Make", "Model", "Color"]):
                    tk.Label(
                        self.table_frame,
                        text=vehicle[key],
                        font=("Poppins", 10),
                        bg=row_color,
                        padx=10,
                        pady=5,
                        anchor="center"
                    ).grid(row=row_idx, column=col_idx, sticky="nsew", ipadx=5, ipady=3)
