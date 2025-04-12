import tkinter as tk
from tkinter import ttk
from database import Database

class ParkingHistoryPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        # Set the background color
        self.config(bg='#F4B738')

        # Title Label
        title_label = tk.Label(self, text="PARKING HISTORY", font=("Poppins", 24, "bold"), bg='#F4B738')
        title_label.pack(pady=50)

        # Navigation Bar
        button_frame = tk.Frame(self, bg='#F4B738')
        button_frame.pack(fill=tk.X, pady=30, padx=30)

        # Adjust the width and height of the buttons
        button_width = 18  # Set the desired width
        button_height = 2  # Set the desired height
        button_font = ("Poppins", 10, "bold")  # Set the font size and make it bold
        button_bg = "#FFFFFF"  # Set the button background color to white
        button_bd = 3  # Set the border width
        button_relief = "raised"  # Set the relief style (options: flat, raised, sunken, groove, ridge)

        tk.Button(button_frame, text="HOME", command=lambda: self.master.show_home(self.user), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="AVAILABLE SLOTS", command=master.show_available_slots, width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="MY VEHICLES", command=lambda: self.master.show_my_vehicles(), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="REGISTER VEHICLE", command=lambda: self.master.show_register_vehicle(),
                  width=button_width, height=button_height, font=button_font, bg=button_bg, bd=button_bd,
                  relief=button_relief).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="LOGOUT", command=lambda: self.master.show_login(), width=button_width,
                  height=button_height, font=button_font, bg=button_bg, bd=button_bd, relief=button_relief).pack(
            side=tk.RIGHT, padx=10, pady=10)

        # Parking History Table
        self.tree = ttk.Treeview(self, columns=("TransactionID", "Slot", "Entry Time", "Exit Time", "Amount"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree.heading("TransactionID", text="Transaction ID")
        self.tree.heading("Slot", text="Slot")
        self.tree.heading("Entry Time", text="Entry Time")
        self.tree.heading("Exit Time", text="Exit Time")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("TransactionID", width=100, anchor="center")
        self.tree.column("Slot", width=50, anchor="center")
        self.tree.column("Entry Time", width=150, anchor="center")
        self.tree.column("Exit Time", width=150, anchor="center")
        self.tree.column("Amount", width=80, anchor="center")

        # Add a style to the Treeview
        style = ttk.Style()
        style.theme_use("default")

        # Style for Treeview
        style.configure("Treeview",
                        background="#fefefe",
                        foreground="#000000",
                        rowheight=40,
                        fieldbackground="#fefefe",
                        bordercolor="#d0d0d0",
                        borderwidth=1)

        # Selected row color
        style.map('Treeview',
                  background=[('selected', '#e0e0e0')],
                  foreground=[('selected', '#000000')])

        # Heading style
        style.configure("Treeview.Heading",
                        background="#E5E4E2",
                        foreground="#000000",
                        font=("Poppins", 10, "bold"))

        # Zebra striping (alternating row color)
        self.tree.tag_configure('oddrow', background='#FFFAFA')
        self.tree.tag_configure('evenrow', background='#EDE9DF')

        self.show_history()


    def show_history(self):
        """Fetch and display parking history for the logged-in user."""
        self.tree.delete(*self.tree.get_children())  # Clear existing entries

        query = """
            SELECT TransactionID, ParkingSlotID, EntryTime, ExitTime, PaymentAmount 
            FROM ParkingTransactions WHERE UserID = %s
        """
        history = self.db.fetch_all(query, (self.user["UserID"],))

        if history:
            for index, record in enumerate(history):
                exit_time = record["ExitTime"] if record["ExitTime"] else "Still Parked"

                # Alternate row colors using tags
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'

                # Safely handle potential missing fields
                self.tree.insert(
                    "", "end",
                    values=(
                        record.get("TransactionID", "N/A"),
                        record.get("ParkingSlotID", "N/A"),
                        record.get("EntryTime", "N/A"),
                        exit_time,
                        f"₱{record.get('PaymentAmount', 0):.2f}"
                    ),
                    tags=(tag,)
                )
        else:
            self.tree.insert("", "end", values=("No data", "", "", "", ""), tags=("evenrow",))


