import tkinter as tk
from database import Database


class HomePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master, bg="#f5b940")  # Yellow background
        self.master = master
        master.geometry("850x500")
        self.user = user
        self.db = Database()

        # Welcome Label (Optional - removed in sample UI, but if you want to keep it uncomment this)
        # tk.Label(self, text=f"Welcome, {self.user['FirstName']} {self.user['LastName']}!", font=("Arial", 14), bg="#f5b940").pack()

        # Title
        tk.Label(self, text="AVAILABLE PARKING SLOT", font=("Arial", 20, "bold"), bg="#f5b940", fg="black").pack(pady=10)

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


        # Slot display
        self.slot_display = tk.Frame(self, bg="#f5b940")
        self.slot_display.pack(pady=10)
        self.display_slots()

    def create_nav_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Arial", 10, "bold"), bg="white", fg="black",
                        relief="flat", padx=10, pady=5, command=command)
        btn.pack(side=tk.LEFT, padx=10)
        btn.configure(highlightbackground="black")
        btn.bind("<Enter>", lambda e: btn.config(relief="sunken"))
        btn.bind("<Leave>", lambda e: btn.config(relief="flat"))

    def display_slots(self):
        """Fetch and display available slots."""
        for widget in self.slot_display.winfo_children():
            widget.destroy()

        slots = self.db.fetch_all("SELECT SlotNumber, IsOccupied FROM ParkingSlots")

        # Container for the table using grid layout
        container_frame = tk.Frame(self.slot_display, bg="#f5b940")
        container_frame.pack(pady=5, fill='both', expand=True)

        # Configure columns for equal weight
        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(1, weight=1)

        # Header
        tk.Label(container_frame, text="Slot No.", font=("Arial", 12, "bold"),
                 bg="#f5b940", width=20, anchor="center", justify="center").grid(row=0, column=0, sticky="nsew", padx=1,
                                                                                 pady=3)

        tk.Label(container_frame, text="Status", font=("Arial", 12, "bold"),
                 bg="#f5b940", width=20, anchor="center", justify="center").grid(row=0, column=1, sticky="nsew", padx=1,
                                                                                 pady=3)

        # Slot Entries
        for index, slot in enumerate(slots, start=1):
            row_bg = "#ffffff" if index % 2 == 1 else "#eeeeee"
            slot_color = "red" if slot["IsOccupied"] else "green"

            tk.Label(container_frame, text=f"Slot {slot['SlotNumber']}", font=("Arial", 11, "bold"),
                     fg=slot_color, bg=row_bg, width=20, anchor="center", relief="flat").grid(row=index, column=0,
                                                                                              sticky="nsew", padx=1,
                                                                                              pady=2)

            tk.Label(container_frame, text="Occupied" if slot["IsOccupied"] else "Available",
                     font=("Arial", 11, "bold"),
                     fg=slot_color, bg=row_bg, width=20, anchor="center", relief="flat").grid(row=index, column=1,
                                                                                              sticky="nsew", padx=1,
                                                                                              pady=2)
