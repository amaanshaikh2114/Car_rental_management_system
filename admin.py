from db import connect_to_db
from tkinter import messagebox

def admin_add_car(model, year, license_plate, rate_per_day):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Car (Model, Year, License_Plate, Rate_per_day) VALUES (%s, %s, %s, %s)", (model, year, license_plate, rate_per_day))
    db.commit()
    new_car_id = cursor.lastrowid       # getting the car id of the newly added car
    cursor.close()
    db.close()
    return new_car_id

def admin_delete_car(car_id):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT Car_ID FROM Car WHERE Car_ID = %s", (car_id,))
    car = cursor.fetchone()
    if car:
        cursor.execute("DELETE FROM Car WHERE Car_ID = %s", (car_id,))
        db.commit()
        cursor.close()
        db.close()
        messagebox.showinfo('Success',f'Car with car ID {car_id} deleted successfully.')
    else:
        messagebox.showinfo('Error',f"Car with car ID {car_id} doesn't exist. Enter the correct car ID.")

def admin_view_bookings():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Rental")
    rentals = cursor.fetchall()
    cursor.close()
    db.close()
    return rentals

def admin_view_transactions():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Payment")
    payments = cursor.fetchall()
    cursor.close()
    db.close()
    return payments
