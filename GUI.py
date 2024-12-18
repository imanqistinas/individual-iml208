import datetime
from tkinter import *
from tkinter import messagebox

# Sample Data
bookings = [{"id": 1, "guest": "Akma", "room": "C2-A", "nights": 3, "base_price": 100, 
             "discount_rate": 0.1, "tax_rate": 0.15, "check_in": "2024-06-01", "check_out": "2024-06-04"},
            {"id": 2, "guest": "Alys", "room": "D4-B", "nights": 5, "base_price": 200, 
             "discount_rate": 0.05, "tax_rate": 0.15, "check_in": "2024-06-05", "check_out": "2024-06-10"}]

# Function to calculate nights between dates
def calculate_nights(check_in, check_out):
    check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d")
    delta = (check_out_date - check_in_date).days
    return max(delta, 0)

# Calculation Functions
def calculate_price(base_price, nights, discount_rate=0):
    return base_price * nights * (1 - discount_rate)

def calculate_total_price(final_price, tax_rate):
    return final_price * (1 + tax_rate)

# CRUD Operations
def create_booking(new_booking):
    bookings.append(new_booking)
    update_listbox()
    messagebox.showinfo("Success", "Booking Added Successfully!")

def update_booking():
    try:
        booking_id = int(entry_id.get())
        for booking in bookings:
            if booking["id"] == booking_id:
                # Update fields
                booking["guest"] = entry_guest.get()
                booking["room"] = entry_room.get()
                booking["check_in"] = entry_check_in.get()
                booking["check_out"] = entry_check_out.get()
                booking["base_price"] = float(entry_base_price.get())
                booking["discount_rate"] = float(entry_discount.get())
                booking["tax_rate"] = float(entry_tax.get())
                booking["nights"] = calculate_nights(booking["check_in"], booking["check_out"])
                update_listbox()
                messagebox.showinfo("Success", "Booking Updated Successfully!")
                return
        messagebox.showerror("Error", "Booking ID not found.")
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all fields are correct.")

def delete_booking():
    try:
        booking_id = int(entry_id.get())
        for i, booking in enumerate(bookings):
            if booking["id"] == booking_id:
                bookings.pop(i)
                update_listbox()
                messagebox.showinfo("Success", "Booking Deleted Successfully!")
                return
        messagebox.showerror("Error", "Booking ID not found.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid Booking ID.")

# Summary Functions
def show_summary():
    total_rev = sum([calculate_total_price(calculate_price(b["base_price"], b["nights"], b["discount_rate"]), b["tax_rate"]) for b in bookings])
    avg_nights = sum([b["nights"] for b in bookings]) / len(bookings) if bookings else 0
    total_count = len(bookings)
    messagebox.showinfo("Summary", f"Total Revenue: RM {total_rev:.2f}\nAverage Nights: {avg_nights:.2f}\nTotal Bookings: {total_count}")

def show_summary():
    total_rev = 0
    avg_nights = 0
    total_count = len(bookings)

    # Generate booking details with check-in and check-out dates
    summary_details = ""
    for booking in bookings:
        total_price = calculate_total_price(calculate_price(booking["base_price"], booking["nights"], booking["discount_rate"]), booking["tax_rate"])
        summary_details += f"ID: {booking['id']}, Guest: {booking['guest']}, Room: {booking['room']}, " \
                           f"Check-in: {booking['check_in']}, Check-out: {booking['check_out']}, " \
                           f"Nights: {booking['nights']}, Total: RM {total_price:.2f}\n"
        total_rev += total_price
        avg_nights += booking["nights"]

    # Calculate the average number of nights
    avg_nights = avg_nights / total_count if total_count > 0 else 0

    # Show the summary
    messagebox.showinfo("Summary", f"Total Revenue: RM {total_rev:.2f}\nAverage Nights: {avg_nights:.2f}\nTotal Bookings: {total_count}\n\n{summary_details}")

# GUI Functions
def add_booking():
    try:
        guest_name = entry_guest.get()
        room = entry_room.get()
        check_in = entry_check_in.get()
        check_out = entry_check_out.get()
        base_price = float(entry_base_price.get())
        discount_rate = float(entry_discount.get())
        tax_rate = float(entry_tax.get())

        nights = calculate_nights(check_in, check_out)
        if nights <= 0:
            messagebox.showerror("Invalid Dates", "Check-out date must be after Check-in date.")
            return

        new_booking = {
            "id": len(bookings) + 1,
            "guest": guest_name,
            "room": room,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "base_price": base_price,
            "discount_rate": discount_rate,
            "tax_rate": tax_rate
        }
        create_booking(new_booking)
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all fields are filled correctly.")

def update_listbox():
    listbox_bookings.delete(0, END)
    for booking in bookings:
        total_price = calculate_total_price(calculate_price(booking["base_price"], booking["nights"], booking["discount_rate"]), booking["tax_rate"])
        listbox_bookings.insert(END, f"ID: {booking['id']}, Guest: {booking['guest']}, Room: {booking['room']}, "
                                    f"Nights: {booking['nights']}, Total: RM {total_price:.2f}")

# GUI Window
root = Tk()
root.title("Airbnb Booking System")
root.geometry("700x600")

# Labels and Entry Fields
Label(root, text="ID (for Update/Delete):").grid(row=0, column=0)
entry_id = Entry(root)
entry_id.grid(row=0, column=1)

Label(root, text="Guest Name:").grid(row=1, column=0)
entry_guest = Entry(root)
entry_guest.grid(row=1, column=1)

Label(root, text="Room:").grid(row=2, column=0)
entry_room = Entry(root)
entry_room.grid(row=2, column=1)

Label(root, text="Check-in Date (YYYY-MM-DD):").grid(row=3, column=0)
entry_check_in = Entry(root)
entry_check_in.grid(row=3, column=1)

Label(root, text="Check-out Date (YYYY-MM-DD):").grid(row=4, column=0)
entry_check_out = Entry(root)
entry_check_out.grid(row=4, column=1)

Label(root, text="Base Price (RM):").grid(row=5, column=0)
entry_base_price = Entry(root)
entry_base_price.grid(row=5, column=1)

Label(root, text="Discount Rate (e.g., 0.1 for 10%):").grid(row=6, column=0)
entry_discount = Entry(root)
entry_discount.grid(row=6, column=1)

Label(root, text="Tax Rate (e.g., 0.15 for 15%):").grid(row=7, column=0)
entry_tax = Entry(root)
entry_tax.grid(row=7, column=1)

# Buttons
Button(root, text="Add Booking", command=add_booking).grid(row=8, column=0, pady=10)
Button(root, text="Update Booking", command=update_booking).grid(row=8, column=1, pady=10)
Button(root, text="Delete Booking", command=delete_booking).grid(row=9, column=0, pady=10)
Button(root, text="Show Summary", command=show_summary).grid(row=9, column=1, pady=10)

# Listbox to Display Bookings
listbox_bookings = Listbox(root, width=100, height=15)
listbox_bookings.grid(row=10, column=0, columnspan=2)

# Populate Listbox with Initial Data
update_listbox()

root.mainloop()
