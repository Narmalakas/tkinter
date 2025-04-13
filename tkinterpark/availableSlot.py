import tkinter as tk
from tkinter import messagebox
from database import Database


class AvailableSlots(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        self.configure(bg="#f4b942")

        tk.Label(self, text="AVAILABLE PARKING SLOTS", font=("Poppins", 24, "bold"), bg="#F4B738").pack(pady=25)

        # Navigation Buttons
        button_frame = tk.Frame(self, bg='#f4b942')
        button_frame.pack(pady=10)

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

        for col in range(len(buttons)):
            button_frame.grid_columnconfigure(col, weight=1)

        self.setup_slot_display()
        self.display_slots()

    def setup_slot_display(self):
        self.canvas = tk.Canvas(self, bg="#e0e0e0", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.slot_display = tk.Frame(self.canvas, bg="#e0e0e0")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.slot_display, anchor="n")

        self.slot_display.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._resize_canvas)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def display_slots(self):
        for widget in self.slot_display.winfo_children():
            widget.destroy()

        slots = self.db.fetch_all("SELECT ParkingSlotID, SlotNumber, IsOccupied FROM ParkingSlots")

        # Header
        header_frame = tk.Frame(self.slot_display, bg="#F4B738")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)
        for col in range(3):
            header_frame.grid_columnconfigure(col, weight=1, uniform="col")

        tk.Label(header_frame, text="Slot No.", font=("Poppins", 11, "bold"), bg="#F4B738").grid(row=0, column=0, padx=5, pady=10)
        tk.Label(header_frame, text="Status", font=("Poppins", 11, "bold"), bg="#F4B738").grid(row=0, column=1, padx=5, pady=10)
        tk.Label(header_frame, text="Action", font=("Poppins", 11, "bold"), bg="#F4B738").grid(row=0, column=2, padx=5, pady=10)

        self.slot_display.grid_columnconfigure(0, weight=1)

        for idx, slot in enumerate(slots, start=1):
            bg_color = "#f9f9f9" if idx % 2 == 0 else "#ffffff"
            row_frame = tk.Frame(self.slot_display, bg=bg_color)
            row_frame.grid(row=idx, column=0, sticky="ew", padx=10, pady=3)

            for col in range(3):
                row_frame.grid_columnconfigure(col, weight=1, uniform="col")

            status_text = "Occupied" if slot["IsOccupied"] else "Available"
            status_color = "red" if slot["IsOccupied"] else "green"

            tk.Label(row_frame, text=f"Slot {slot['SlotNumber']}", font=("Poppins", 11, "bold"),
                     bg=bg_color).grid(row=0, column=0, padx=5, pady=10)

            tk.Label(row_frame, text=status_text, font=("Poppins", 10, "bold"),
                     fg=status_color, bg=bg_color).grid(row=0, column=1, padx=5, pady=10)

            action_btn_kwargs = {
                "font": ("Poppins", 10, "bold"),
                "relief": "groove",
                "bg": "white",
                "fg": "black",
                "padx": 10,
                "pady": 2
            }

            action_button = None
            if slot["IsOccupied"]:
                parked_user = self.db.fetch_one("""
                    SELECT UserID FROM ParkingTransactions 
                    WHERE ParkingSlotID = %s AND ExitTime IS NULL
                """, (slot["ParkingSlotID"],))

                if parked_user and parked_user.get("UserID") == self.user.get("UserID"):
                    action_button = tk.Button(row_frame, text="Park Out",
                                              command=lambda s=slot["ParkingSlotID"]: self.park_out(s),
                                              **action_btn_kwargs)
            else:
                action_button = tk.Button(row_frame, text="Park",
                                          command=lambda s=slot["ParkingSlotID"]: self.park_vehicle(s),
                                          **action_btn_kwargs)

            if action_button:
                action_button.grid(row=0, column=2, padx=5, pady=5)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def park_vehicle(self, slot_id):
        """Popup window for parking transaction - Yellow Themed Modern UI"""
        popup = tk.Toplevel(self)
        popup.title("Park Vehicle")
        popup.geometry("400x500")
        popup.configure(bg="#F4B738")  # Light yellow background
        popup.resizable(False, False)

        main_frame = tk.Frame(popup, bg="#F4B738")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        header = tk.Label(main_frame, text=f"PARK IN SLOT {slot_id}", font=("Arial", 16, "bold"), bg="#F4B738",fg="#333")
        header.pack(pady=(0, 10))

        vehicles = self.db.fetch_all(""" 
            SELECT VehicleID, Make, Model, LicensePlate 
            FROM Vehicles 
            WHERE UserID = %s 
            AND VehicleID NOT IN (SELECT VehicleID FROM ParkingTransactions WHERE ExitTime IS NULL)
        """, (self.user["UserID"],))

        if not vehicles:
            tk.Label(main_frame, text="No available vehicles to park!", fg="red", bg="#F4B738",
                     font=("Arial", 12)).pack()
            return

        # Vehicle selection
        tk.Label(main_frame, text="Select Vehicle:", bg="#F4B738", font=("Arial", 11, "bold")).pack(anchor="w")
        self.selected_vehicle = tk.StringVar()
        vehicle_options = {f"{v['Make']} {v['Model']} ({v['LicensePlate']})": v["VehicleID"] for v in vehicles}
        vehicle_dropdown = ttk.Combobox(main_frame, textvariable=self.selected_vehicle,
                                        values=list(vehicle_options.keys()), state="readonly")
        vehicle_dropdown.pack(fill="x", pady=5)

        # Entry time
        tk.Label(main_frame, text="Entry Date & Time:", bg="#F4B738", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        entry_frame = tk.Frame(main_frame, bg="#F4B738")
        entry_frame.pack(fill="x")
        self.entry_date = DateEntry(entry_frame, date_pattern="yyyy-mm-dd")
        self.entry_date.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.entry_time = ttk.Combobox(entry_frame, values=[f"{h:02d}:00" for h in range(24)], state="readonly")
        self.entry_time.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Exit time
        tk.Label(main_frame, text="Exit Date & Time:", bg="#F4B738", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        exit_frame = tk.Frame(main_frame, bg="#F4B738")
        exit_frame.pack(fill="x")
        self.exit_date = DateEntry(exit_frame, date_pattern="yyyy-mm-dd")
        self.exit_date.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.exit_time = ttk.Combobox(exit_frame, values=[f"{h:02d}:00" for h in range(24)], state="readonly")
        self.exit_time.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Discount
        tk.Label(main_frame, text="Select Discount:", bg="#F4B738", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.discount_var = tk.StringVar(value="None")
        discount_options = ["None", "Student", "Faculty", "PWD", "Visitor"]
        discount_dropdown = ttk.Combobox(main_frame, textvariable=self.discount_var, values=discount_options,state="readonly")
        discount_dropdown.pack(fill="x", pady=5)
        discount_dropdown.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        # Payment label
        self.payment_label = tk.Label(main_frame, text="PAYMENT: ₱0", font=("Arial", 12, "bold"), bg="#F4B738", fg="#444")
        self.payment_label.pack(pady=10)

        # Payment method
        tk.Label(main_frame, text="Payment Method:", bg="#F4B738", font=("Arial", 11,"bold")).pack(anchor="w")
        self.payment_method = tk.StringVar(value="Cash")
        payment_methods = ["Cash", "Online Payment", "Credit Card"]
        payment_dropdown = ttk.Combobox(main_frame, textvariable=self.payment_method, values=payment_methods,state="readonly")
        payment_dropdown.pack(fill="x", pady=5)

        # Bindings for calculation
        self.entry_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.entry_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())
        self.exit_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.exit_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        # Confirm button
        confirm_btn = tk.Button(main_frame,
                                text="CONFIRM PARKING",
                                font=("Poppins", 12, "bold"),
                                bg="#F4B738",
                                fg="black",
                                bd=2,  # Set border width
                                relief="solid",  # Set relief style (solid, raised, sunken, etc.)
                                command=lambda: self.confirm_parking(slot_id, vehicle_options, popup))
        confirm_btn.pack(pady=15, ipadx=10, ipady=5)

    def calculate_payment(self):
        try:
            entry_datetime = datetime.strptime(f"{self.entry_date.get()} {self.entry_time.get()}", "%Y-%m-%d %H:%M")
            exit_datetime = datetime.strptime(f"{self.exit_date.get()} {self.exit_time.get()}", "%Y-%m-%d %H:%M")

            if exit_datetime <= entry_datetime:
                self.payment_label.config(text="Payment: ₱0")
                return

            total_hours = max(1, int((exit_datetime - entry_datetime).total_seconds() / 3600))
            base_amount = total_hours * 20
            discount_rates = {"Student": 0.20, "Faculty": 0.15, "PWD": 0.30, "Visitor": 0.10, "None": 0.00}
            discount = discount_rates.get(self.discount_var.get(), 0) * base_amount
            total_amount = base_amount - discount

            self.payment_label.config(text=f"Payment: ₱{total_amount:.2f}")
        except ValueError:
            self.payment_label.config(text="Payment: ₱0")

    def confirm_parking(self, slot_id, vehicles, popup):
        if not self.selected_vehicle.get():
            messagebox.showerror("Error", "Please select a vehicle.")
            return

        try:
            vehicle_id = vehicles[self.selected_vehicle.get()]
            entry_datetime = datetime.strptime(f"{self.entry_date.get()} {self.entry_time.get()}", "%Y-%m-%d %H:%M")
            exit_datetime = datetime.strptime(f"{self.exit_date.get()} {self.exit_time.get()}", "%Y-%m-%d %H:%M")

            if exit_datetime <= entry_datetime:
                messagebox.showerror("Error", "Exit time must be later than entry time.")
                return

            # Calculate payment
            total_hours = max(1, int((exit_datetime - entry_datetime).total_seconds() / 3600))
            base_amount = total_hours * 20
            discount_rates = {"Student": 0.20, "Faculty": 0.15, "PWD": 0.30, "Visitor": 0.10, "None": 0.00}
            discount = discount_rates.get(self.discount_var.get(), 0) * base_amount
            total_amount = base_amount - discount
            discount_rate = discount_rates.get(self.discount_var.get(), 0)

            payment_method = self.payment_method.get()

            # Insert into ParkingTransactions
            query = """
            INSERT INTO ParkingTransactions (UserID, VehicleID, ParkingSlotID, EntryTime, ExitTime, PaymentAmount, PaymentMethod, DiscountRate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute(query, (
                self.user["UserID"], vehicle_id, slot_id, entry_datetime, None, total_amount, payment_method,
                discount_rate
            ))

            # Update the slot to occupied
            self.db.execute("UPDATE ParkingSlots SET IsOccupied = TRUE WHERE ParkingSlotID = %s", (slot_id,))

            messagebox.showinfo("Success", "Vehicle parked successfully!")
            popup.destroy()
            self.display_slots()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def park_out(self, slot_id):
        """Park out the vehicle and free the parking slot"""
        try:
            # Update the parking transaction with ExitTime
            exit_time = datetime.now()
            self.db.execute("""
                UPDATE ParkingTransactions 
                SET ExitTime = %s 
                WHERE ParkingSlotID = %s AND ExitTime IS NULL
            """, (exit_time, slot_id))

            # Update the slot to available
            self.db.execute("""
                UPDATE ParkingSlots 
                SET IsOccupied = FALSE 
                WHERE ParkingSlotID = %s
            """, (slot_id,))

            messagebox.showinfo("Success", "Vehicle has been parked out successfully!")
            self.display_slots()  # Refresh the slot display automatically
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
