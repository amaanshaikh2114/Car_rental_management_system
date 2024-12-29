from db import connect_to_db
from tkinter import messagebox
import mysql.connector

def customer_rent_car(customer_id, car_id, no_of_days):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute('SELECT Status FROM Car WHERE Car_ID = %s', (car_id,))  # Corrected line
    result = cursor.fetchone()  # Fetch the status value directly
    print(result)
    if result != None:
        status = result[0]
        if status == 'available':
            cursor.execute("INSERT INTO Rental (Customer_ID, Car_ID, Issue_date, Return_date, No_of_days) VALUES (%s, %s, CURDATE(), CURDATE() + INTERVAL %s DAY, %s)", (customer_id, car_id, no_of_days, no_of_days))
            rental_id = cursor.lastrowid
            cursor.execute("UPDATE Car SET Status = 'rented' WHERE Car_ID = %s", (car_id,))
            db.commit()
            cursor.close()
            db.close()
            return rental_id
        elif status == 'rented':
            # getting last customer who booked the car
            cursor.execute('SELECT Customer_ID FROM Rental WHERE Car_ID = %s ORDER BY Issue_date DESC LIMIT 1', (car_id,))      
            cust = cursor.fetchone()
            # print(cust)
            if cust[0] == customer_id:
                print('Already booked')
                messagebox.showerror('Error','You have already booked the requested car!')
            else:
                messagebox.showerror('Car not booked','Requested car is currently not available for booking!')
            return -1
    else:
        messagebox.showerror('Error', f"Car with ID {car_id} doesn't exist. Enter the correct rental ID.")
        return -1


def customer_return_car(customer_id, rental_id):
    db = connect_to_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT Customer_ID FROM Rental WHERE Rental_ID = %s", (rental_id,))
        cust_id = cursor.fetchone()[0]
        if int(cust_id) == int(customer_id): 
            cursor.execute("SELECT Car_ID FROM Rental WHERE Rental_ID = %s", (rental_id,))
            car_id = cursor.fetchone()[0]
            cursor.execute("UPDATE Car SET Status = 'Available' WHERE Car_ID = %s", (car_id,))
            cursor.execute("UPDATE Rental SET Status = 'Returned' WHERE Rental_ID = %s", (rental_id,))
            db.commit()
            messagebox.showinfo('Car returned successfully', f'Your car in rental ID {rental_id} has been returned.')
        else:
            messagebox.showerror('Car not returned', f'Car in rental ID {rental_id} has not been booked by you. Enter the correct rental ID.')

        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    finally:
        cursor.close()
        db.close()


def customer_view_bookings(customer_id):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Rental WHERE Customer_ID = %s", (customer_id,))
    rentals = cursor.fetchall()
    cursor.close()
    db.close()
    return rentals

def customer_view_cars():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Car WHERE Status = 'available'")
    cars = cursor.fetchall()
    cursor.close()
    db.close()
    return cars

def generate_payment(rental_id, amount):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Payment (Rental_ID, Payment_Date, Amount) VALUES (%s, CURDATE(), %s)", (rental_id, amount))
    db.commit()
    cursor.close()
    db.close()
