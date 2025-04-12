import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from database import Database
from datetime import datetime, timedelta

class AvailableSlots(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        self.configure(bg="#f4b942")  # Set yellow background

        tk.Label(self, text="AVAILABLE PARKING SLOTS", font=("Poppins", 24, "bold"), bg="#F4B738").pack(pady=25)

        # Navigation Buttons
        button_frame = tk.Frame(self, bg='#f4b942')
        button_frame.pack(pady=10)

        # Create a grid with 5 centered buttons
        buttons = [
            ("HOME", self.master.show_home),
            ("MY VEHICLE", self.master.show_my_vehicles),
            ("REGISTER VEHICLE", self.master.show_register_vehicle),
            ("PARKING HISTORY", self.master.show_parking_history),
            ("LOG OUT", self.master.show_login)
        ]

        for col, (text, command) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                command=command,
                width=18,
                height=2,
                font=("Poppins", 10, "bold"),
                bg="#FFFFFF",
                bd=3,
                relief="raised"
            ).grid(row=0, column=col, padx=10, pady=10)

        # Center the button_frame using grid options
        button_frame.grid_columnconfigure(tuple(range(len(buttons))), weight=1)

        # Parking Slots Display
        self.slot_display = tk.Frame(self, bg="#f4b942")
        self.slot_display.pack(pady=10)
        self.display_slots()

    def create_shadow_button(self, parent, text, command=None):
        """Creates a white button with drop shadow"""
        canvas = tk.Canvas(parent, width=145, height=40, bg="#f4b942", highlightthickness=0)
        canvas.pack_propagate(False)

        # Shadow
        canvas.create_rectangle(6, 6, 140, 35, fill="black", outline="black")

        # Main Button
        canvas.create_rectangle(0, 0, 134, 30, fill="white", outline="black")
        canvas.create_text(67, 15, text=text, font=("Poppins", 10, "bold"))

        # Click event
        if command:
            canvas.bind("<Button-1>", lambda event: command())

        return canvas

    def display_slots(self):
        for widget in self.slot_display.winfo_children():
            widget.destroy()

        slots = self.db.fetch_all("SELECT ParkingSlotID, SlotNumber, IsOccupied FROM ParkingSlots")

        # Header
        header_frame = tk.Frame(self.slot_display, bg="#F4B738")
        header_frame.pack(fill="x", pady=5)

        tk.Label(header_frame, text="Slot No.", font=("Poppins", 12, "bold"), bg="#F4B738", width=20).grid(row=0, column=0)
        tk.Label(header_frame, text="Status", font=("Poppins", 12, "bold"), bg="#F4B738", width=20).grid(row=0, column=1)
        tk.Label(header_frame, text="Action", font=("Poppins", 12, "bold"), bg="#F4B738", width=20).grid(row=0, column=2)

        # Rows
        for idx, slot in enumerate(slots):
            bg_color = "#f2f2f2" if idx % 2 == 0 else "#ffffff"
            row_frame = tk.Frame(self.slot_display, bg=bg_color)
            row_frame.pack(fill="x")

            status_text = "Occupied" if slot["IsOccupied"] else "Available"
            status_color = "red" if slot["IsOccupied"] else "green"

            slot_label = tk.Label(row_frame, text=f"Slot {slot['SlotNumber']}", font=("Poppins", 11, "bold"),
                                  fg=status_color, bg=bg_color, width=20)
            slot_label.grid(row=0, column=0, padx=2, pady=1, sticky="nsew")

            status_label = tk.Label(row_frame, text=status_text, font=("Poppins", 11),
                                    fg=status_color, bg=bg_color, width=20)
            status_label.grid(row=0, column=1, padx=2, pady=1, sticky="nsew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=2, padx=2, pady=1, sticky="nsew")

            if slot["IsOccupied"]:
                parked_user = self.db.fetch_one("""
                    SELECT UserID 
                    FROM ParkingTransactions 
                    WHERE ParkingSlotID = %s AND ExitTime IS NULL
                """, (slot["ParkingSlotID"],))

                if parked_user and parked_user["UserID"] == self.user["UserID"]:
                    tk.Button(action_frame, text="Park Out", font=("Poppins", 10, "bold"),
                              relief="groove", bg="white", fg="black",
                              command=lambda s=slot["ParkingSlotID"]: self.park_out(s)).pack(padx=5)
            else:
                tk.Button(action_frame, text="Park", font=("Poppins", 10, "bold"),
                          relief="groove", bg="white", fg="black",
                          command=lambda s=slot["ParkingSlotID"]: self.park_vehicle(s)).pack(padx=5)

    def park_vehicle(self, slot_id):
        """Popup window for parking transaction (Styled)"""
        popup = tk.Toplevel(self)
        popup.title(f"Park in Slot {slot_id}")
        popup.geometry("400x520")
        popup.configure(bg="#f5b918")  # Yellow background

        # Container
        container = tk.Frame(popup, bg="white", bd=0, relief="flat")
        container.place(relx=0.5, rely=0.5, anchor="center", width=360, height=480)

        tk.Label(container, text=f"PARKING SLOT {slot_id}", font=("Helvetica", 16, "bold"), bg="white",
                 fg="black").pack(pady=(20, 10))

        # Fetch vehicles not currently parked
        vehicles = self.db.fetch_all(""" 
            SELECT VehicleID, Make, Model, LicensePlate 
            FROM Vehicles 
            WHERE UserID = %s 
            AND VehicleID NOT IN (SELECT VehicleID FROM ParkingTransactions WHERE ExitTime IS NULL)
            """, (self.user["UserID"],))

        if not vehicles:
            tk.Label(container, text="No available vehicles to park!", fg="red", bg="white").pack(pady=10)
            return

        # Vehicle selection
        tk.Label(popup, text="Select Vehicle:", bg="white").pack()
        self.selected_vehicle = tk.StringVar()
        vehicle_options = {f"{v['Make']} {v['Model']} ({v['LicensePlate']})": v["VehicleID"] for v in vehicles}
        vehicle_dropdown = ttk.Combobox(container, textvariable=self.selected_vehicle, values=list(vehicle_options.keys()), state="readonly")
        vehicle_dropdown.pack(pady=5)

        # Entry Date & Time
        tk.Label(container, text="Entry Date & Time:", bg="white").pack()
        self.entry_date = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.entry_date.pack(pady=2)
        self.entry_time = ttk.Combobox(container, values=[f"{h:02d}:00" for h in range(24)], state="readonly")
        self.entry_time.pack(pady=2)

        # Exit Date & Time
        tk.Label(container, text="Exit Date & Time:", bg="white").pack()
        self.exit_date = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.exit_date.pack(pady=2)
        self.exit_time = ttk.Combobox(container, values=[f"{h:02d}:00" for h in range(24)], state="readonly")
        self.exit_time.pack(pady=2)

        # Discount Selection
        tk.Label(container, text="Select Discount:", bg="white").pack()
        self.discount_var = tk.StringVar(value="None")
        discount_options = ["None", "Student", "Faculty", "PWD", "Visitor"]
        discount_dropdown = ttk.Combobox(container, textvariable=self.discount_var, values=discount_options,
                                         state="readonly")
        discount_dropdown.pack(pady=2)
        discount_dropdown.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        # Payment Display
        self.payment_label = tk.Label(container, text="Payment: ₱0", font=("Helvetica", 13, "bold"), bg="white",
                                      fg="black")
        self.payment_label.pack(pady=8)

        # Payment Method
        tk.Label(container, text="Payment Method:", bg="white").pack()
        self.payment_method = tk.StringVar(value="Cash")
        payment_methods = ["Cash", "Online Payment", "Credit Card"]
        payment_dropdown = ttk.Combobox(container, textvariable=self.payment_method, values=payment_methods,
                                        state="readonly")
        payment_dropdown.pack(pady=2)

        # Bindings for auto calculation
        self.entry_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.entry_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())
        self.exit_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.exit_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        # Confirm button
        confirm_btn = tk.Button(container, text="Confirm Parking", font=("Helvetica", 10, "bold"),
                                bg="#f5b918", activebackground="#e0a800", relief="raised",
                                command=lambda: self.confirm_parking(slot_id, vehicle_options, popup))
        confirm_btn.pack(pady=15)
