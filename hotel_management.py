import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class HotelManagementSystem:
    def __init__(self, master):
        self.master = master
        master.title("Hotel Management System")

        self.conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="hotel_management"
        )
        self.cursor = self.conn.cursor()
        self.main_frame = tk.Frame(master)
        self.main_frame.pack()

        self.welcome_label = tk.Label(self.main_frame, text="WELCOME", font=("Arial", 24))
        self.welcome_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack()

        self.check_in_button = tk.Button(self.buttons_frame, text="Check In", command=self.check_in, width=15)
        self.check_in_button.pack(side="left", padx=10, pady=10)

        self.show_guest_list_button = tk.Button(self.buttons_frame, text="Show Guest List", command=self.show_guest_list, width=15)
        self.show_guest_list_button.pack(side="left", padx=10, pady=10)

        self.check_out_button = tk.Button(self.buttons_frame, text="Check Out", command=self.check_out, width=15)
        self.check_out_button.pack(side="left", padx=10, pady=10)

        self.get_info_button = tk.Button(self.buttons_frame, text="Get Info", command=self.get_info, width=15)
        self.get_info_button.pack(side="left", padx=10, pady=10)

        self.exit_button = tk.Button(self.buttons_frame, text="Exit", command=master.quit, width=15)
        self.exit_button.pack(side="left", padx=10, pady=10)

    def check_in(self):
        self.check_in_window = tk.Toplevel(self.master)
        self.check_in_window.title("Check In")

        self.name_label = tk.Label(self.check_in_window, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.check_in_window)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.address_label = tk.Label(self.check_in_window, text="Address:")
        self.address_label.grid(row=1, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(self.check_in_window)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5)

        self.phone_label = tk.Label(self.check_in_window, text="Phone:")
        self.phone_label.grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.check_in_window)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        self.room_label = tk.Label(self.check_in_window, text="Room Type:")
        self.room_label.grid(row=3, column=0, padx=5, pady=5)
        self.room_var = tk.StringVar(self.check_in_window)
        self.room_var.set("Deluxe") 
        self.room_options = ["Deluxe", "General", "Full Deluxe", "Joint"]
        self.room_dropdown = ttk.Combobox(self.check_in_window, textvariable=self.room_var, values=self.room_options)
        self.room_dropdown.grid(row=3, column=1, padx=5, pady=5)

        self.days_label = tk.Label(self.check_in_window, text="Number of Days:")
        self.days_label.grid(row=4, column=0, padx=5, pady=5)
        self.days_entry = tk.Entry(self.check_in_window)
        self.days_entry.grid(row=4, column=1, padx=5, pady=5)

        self.payment_label = tk.Label(self.check_in_window, text="Payment Method:")
        self.payment_label.grid(row=5, column=0, padx=5, pady=5)
        self.payment_var = tk.StringVar(self.check_in_window)
        self.payment_var.set("Cash") 
        self.payment_options = ["Cash", "Credit/Debit Card"]
        self.payment_dropdown = ttk.Combobox(self.check_in_window, textvariable=self.payment_var, values=self.payment_options)
        self.payment_dropdown.grid(row=5, column=1, padx=5, pady=5)
        
        self.submit_button = tk.Button(self.check_in_window, text="Submit", command=self.submit_check_in)
        self.submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def submit_check_in(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        room_type = self.room_var.get()
        days = self.days_entry.get()
        payment_method = self.payment_var.get()

        if not name or not address or not phone or not room_type or not days or not payment_method:
            messagebox.showerror("Error", "Please fill all the fields.")
            return
        try:
            self.cursor.execute(
                "INSERT INTO guests (name, address, phone, room_type, days, payment_method) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, address, phone, room_type, days, payment_method)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Check In successful!")
            self.check_in_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to insert data: {err}")

    def show_guest_list(self):
        self.guest_list_window = tk.Toplevel(self.master)
        self.guest_list_window.title("Guest List")

        self.guest_list_treeview = ttk.Treeview(self.guest_list_window, columns=("Name", "Address", "Phone", "Room Type", "Days", "Payment Method"), show="headings")
        self.guest_list_treeview.heading("Name", text="Name")
        self.guest_list_treeview.heading("Address", text="Address")
        self.guest_list_treeview.heading("Phone", text="Phone")
        self.guest_list_treeview.heading("Room Type", text="Room Type")
        self.guest_list_treeview.heading("Days", text="Days")
        self.guest_list_treeview.heading("Payment Method", text="Payment Method")
        self.guest_list_treeview.pack()

        self.cursor.execute("SELECT * FROM guests")
        guests = self.cursor.fetchall()

        for guest in guests:
            self.guest_list_treeview.insert("", "end", values=guest)

    def check_out(self):
        self.check_out_window = tk.Toplevel(self.master)
        self.check_out_window.title("Check Out")

        self.guest_id_label = tk.Label(self.check_out_window, text="Guest ID:")
        self.guest_id_label.grid(row=0, column=0, padx=5, pady=5)

        self.guest_id_entry = tk.Entry(self.check_out_window)
        self.guest_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.check_out_window, text="Submit", command=self.submit_check_out)
        self.submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    def submit_check_out(self):
        guest_id = self.guest_id_entry.get()

        if not guest_id:
            messagebox.showerror("Error", "Please enter the Guest ID.")
            return

        try:
            self.cursor.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Check Out successful!")

            self.check_out_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete guest: {err}")

    def get_info(self):
        self.get_info_window = tk.Toplevel(self.master)
        self.get_info_window.title("Get Info")

        self.guest_id_label = tk.Label(self.get_info_window, text="Guest ID:")
        self.guest_id_label.grid(row=0, column=0, padx=5, pady=5)

        self.guest_id_entry = tk.Entry(self.get_info_window)
        self.guest_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self.get_info_window, text="Submit", command=self.submit_get_info)
        self.submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    def submit_get_info(self):
        guest_id = self.guest_id_entry.get()

        if not guest_id:
            messagebox.showerror("Error", "Please enter the Guest ID.")
            return

        try:
            self.cursor.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
            guest = self.cursor.fetchone()

            if guest:
                info = f"Name: {guest[1]}\nAddress: {guest[2]}\nPhone: {guest[3]}\nRoom Type: {guest[4]}\nDays: {guest[5]}\nPayment Method: {guest[6]}"
                messagebox.showinfo("Guest Info", info)
            else:
                messagebox.showerror("Error", "Guest not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch guest data: {err}")

root = tk.Tk()
app = HotelManagementSystem(root)
root.mainloop()
