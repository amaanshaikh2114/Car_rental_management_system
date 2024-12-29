from tkinter import *
from tkinter import messagebox, Text, END
import tkinter as tk
import mysql.connector
from db import connect_to_db
from admin import admin_add_car, admin_delete_car, admin_view_bookings, admin_view_transactions
from customer import customer_rent_car, customer_return_car, customer_view_bookings, customer_view_cars, generate_payment

def login_screen():
    global reg_user_type_var, reg_user_name_entry, reg_user_phone_entry, reg_user_email_entry, reg_password_entry, user_id_entry, password_entry, user_type_var

    root = tk.Tk()
    root.title("Car Rental System - Login")

    label_font = ("Helvetica", 13)
    entry_font = ("Helvetica", 13)
    button_font = ("Helvetica", 13)

    # Creating a Frame to hold the widgets
    frame1 = tk.LabelFrame(master=root, text="Register here")
    frame1.grid(row=0, column=0, pady=10, padx=10)

    tk.Label(frame1, text="Name:", font=label_font).grid(row=0, column=0, pady=10, padx=10)
    reg_user_name_entry = tk.Entry(frame1, font=entry_font, width=20)
    reg_user_name_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame1, text="Phone No:", font=label_font).grid(row=1, column=0, pady=10, padx=10)
    reg_user_phone_entry = tk.Entry(frame1, font=entry_font, width=20)
    reg_user_phone_entry.grid(row=1, column=1, pady=10, padx=10)

    tk.Label(frame1, text="Email:", font=label_font).grid(row=2, column=0, pady=10, padx=10)
    reg_user_email_entry = tk.Entry(frame1, font=entry_font, width=20)
    reg_user_email_entry.grid(row=2, column=1, pady=10, padx=10)

    tk.Label(frame1, text="Password:", font=label_font).grid(row=3, column=0, pady=10, padx=10)
    reg_password_entry = tk.Entry(frame1, show='*', font=entry_font, width=20)
    reg_password_entry.grid(row=3, column=1, pady=10, padx=10)

    tk.Label(frame1, text="Register as:", font=label_font).grid(row=4, column=0, pady=10, padx=10)

    reg_user_type_var = tk.StringVar(value=False)
    tk.Radiobutton(frame1, text="Customer", variable=reg_user_type_var, value=False, font=label_font).grid(row=5, column=0, pady=10, padx=10)
    tk.Radiobutton(frame1, text="Admin", variable=reg_user_type_var, value=True, font=label_font).grid(row=5, column=1, pady=10, padx=10)

    tk.Button(frame1, text="Register", command=register_customer, font=button_font, width=10).grid(row=6, column=0, columnspan=2, pady=20)

    # Creating a Frame to hold the login widgets
    frame2 = tk.LabelFrame(master=root, text="Login here")
    frame2.grid(row=1, column=0, pady=10, padx=10)

    tk.Label(frame2, text="User ID:", font=label_font).grid(row=0, column=0, pady=10, padx=10)
    user_id_entry = tk.Entry(frame2, font=entry_font, width=20)
    user_id_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame2, text="Password:", font=label_font).grid(row=1, column=0, pady=10, padx=10)
    password_entry = tk.Entry(frame2, show='*', font=entry_font, width=20)
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    user_type_var = tk.StringVar(value="Customer")
    tk.Radiobutton(frame2, text="Customer", variable=user_type_var, value="Customer", font=label_font).grid(row=2, column=0, pady=10, padx=10)
    tk.Radiobutton(frame2, text="Admin", variable=user_type_var, value="Admin", font=label_font).grid(row=2, column=1, pady=10, padx=10)

    tk.Button(frame2, text="Login", command=login, font=button_font, width=10).grid(row=3, column=0, columnspan=2, pady=20)

    root.mainloop()

def register_customer():
    name = reg_user_name_entry.get()
    phone = reg_user_phone_entry.get()
    email = reg_user_email_entry.get()
    password = reg_password_entry.get()
    user_type = reg_user_type_var.get()
    
    if name and phone and password:
        try:
            # Establish a connection to the MySQL database
            conn = connect_to_db()
            cursor = conn.cursor()

            # Insert the new customer into the database
            if email:
                cursor.execute("INSERT INTO Customer (Name, Phone, Email, Password, Is_Admin) VALUES (%s, %s, %s, %s, %s)", (name, phone, email, password, user_type))
                conn.commit()
            else:
                cursor.execute("INSERT INTO Customer (Name, Phone, Password, Is_Admin) VALUES (%s, %s, %s, %s)", (name, phone, password, user_type))
                conn.commit()
            
            new_cust_id = cursor.lastrowid      # getting the customer id of the newly created customer
            messagebox.showinfo("Registration successful", f"Your generated customer ID: {new_cust_id}")
            reg_user_name_entry.delete(0, tk.END)
            reg_user_phone_entry.delete(0, tk.END)
            reg_user_email_entry.delete(0, tk.END)
            reg_password_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill out all fields")


def login():
    user_id = user_id_entry.get()
    password = password_entry.get()
    user_type = user_type_var.get()
    
    if user_id and password:
        try:
            # Establish a connection to the MySQL database
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT Password FROM Customer WHERE Customer_ID = %s", (user_id,))
            result = cursor.fetchone()
            if result and result[0] == password:
                cursor.execute("SELECT Is_Admin FROM Customer WHERE Customer_ID = %s", (user_id,))
                result = cursor.fetchone()
                if user_type == 'Customer' and result[0] == 0:
                    customer_dashboard(int(user_id))
                elif user_type == 'Admin' and result[0] == 1:
                    admin_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid user type login!")

            else:
                messagebox.showerror("Error", "Invalid credentials!")
         
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill out all fields!")


def admin_dashboard():
    root = Tk()
    root.title("Admin Dashboard")

    def add_car():
        model = entry_model.get()
        year = entry_year.get()
        license_plate = entry_license_plate.get()
        rate_per_day = entry_rate_per_day.get()
        new_car_id = admin_add_car(model, year, license_plate, rate_per_day)
        messagebox.showinfo('Car added successfully', f'Car ID for newly added car: {new_car_id}')

    def delete_car():
        car_id = entry_car_id.get()
        admin_delete_car(car_id)
        
    def view_bookings():
        bookings = admin_view_bookings()
        text_area.delete('1.0', END)
        for booking in bookings:
            text_area.insert(END, f"{booking}\n")
        label_message.config(text="|       Rental_ID       |       Customer_ID       |       Car_ID       |       Issue_date       |       Return_date       |       No_of_days       |       Status      |", fg="black")

    def view_transactions():
        transactions = admin_view_transactions()
        text_area.delete('1.0', END)
        for transaction in transactions:
            text_area.insert(END, f"{transaction}\n")
        label_message.config(text="|       Payment_ID       |       Rental_ID       |       Payment_Date       |       Amount       |", fg="black")

    def view_cars():
        cars = customer_view_cars()
        text_area.delete('1.0', END)
        for car in cars:
            text_area.insert(END, f"{car}\n")
        label_message.config(text="|            Car_ID              |            Model            |        Year       |           License_Plate          |          Status          |       Rate_per_day       |", fg="black")


    frame1 = Frame(root)
    frame1.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    button_view_cars = Button(frame1, text="View Available Cars", command=view_cars)
    button_view_cars.pack(pady=10)

    button_view_bookings = Button(frame1, text="View Bookings", command=view_bookings)
    button_view_bookings.pack(pady=10)

    button_view_transactions = Button(frame1, text="View Transactions", command=view_transactions)
    button_view_transactions.pack(pady=10)

    center_frame = Frame(root)
    center_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
    frame2 = LabelFrame(center_frame, text='Add a new car here')
    frame2.grid(row=0, column=0, padx=75, pady=10)
    label_model = Label(frame2, text="Model")
    label_model.pack(pady=5)
    entry_model = Entry(frame2, borderwidth=2)
    entry_model.pack(padx=10,pady=5)

    label_year = Label(frame2, text="Year")
    label_year.pack(pady=5)
    entry_year = Entry(frame2, borderwidth=2)
    entry_year.pack(padx=10,pady=5)

    label_license_plate = Label(frame2, text="License Plate")
    label_license_plate.pack(pady=5)
    entry_license_plate = Entry(frame2, borderwidth=2)
    entry_license_plate.pack(padx=10,pady=5)

    label_rate_per_day = Label(frame2, text="Rate per Day")
    label_rate_per_day.pack(pady=5)
    entry_rate_per_day = Entry(frame2, borderwidth=2)
    entry_rate_per_day.pack(padx=10,pady=5)

    button_add_car = Button(frame2, text="Add Car", command=add_car)
    button_add_car.pack(pady=15)

    frame3 = LabelFrame(center_frame, text='Delete a car here')
    frame3.grid(row=0, column=1, padx=75, pady=10)
    label_car_id = Label(frame3, text="Car ID (for deletion)")
    label_car_id.pack(pady=5)
    entry_car_id = Entry(frame3, borderwidth=2)
    entry_car_id.pack(padx=10,pady=5)

    button_delete_car = Button(frame3, text="Delete Car", command=delete_car)
    button_delete_car.pack(pady=10)

    label_message = Label(root, text="", borderwidth=1, relief='solid')
    label_message.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    text_area = Text(root, height=10, width=85)
    text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


def customer_dashboard(customer_id):
    root = tk.Tk()
    root.title("Customer Dashboard")

    def rent_car():
        car_id = entry_car_id.get()
        no_of_days = entry_no_of_days.get()
        rental_id = customer_rent_car(customer_id, car_id, no_of_days)
        if rental_id != -1:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT Rate_per_day FROM Car WHERE Car_ID = %s", (car_id,))           
            # print(result)
            entry_rate_per_day = cursor.fetchone()[0]
            total = int(no_of_days) * int(entry_rate_per_day)
            generate_payment(rental_id, total)
            messagebox.showinfo('Car rented successfully', f'Your rental for INR {total} has been generated.')

    def return_car():
        rent_id = entry_rental_id.get()
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute('SELECT Rental_ID FROM Rental WHERE Rental_ID = %s', (rent_id,))
        existing_rent = cursor.fetchone()
        if existing_rent != None: 
            rental_id = existing_rent[0]
            customer_return_car(customer_id, rental_id)
        else:
            messagebox.showerror('Error', f"Rental ID {rent_id} doesn't exist. Enter the correct rental ID.")


    def view_bookings():
        bookings = customer_view_bookings(customer_id)
        text_area.delete('1.0', END)
        for booking in bookings:
            text_area.insert(END, f"{booking}\n")
        label_message.config(text="|       Rental_ID       |       Customer_ID       |       Car_ID       |       Issue_date       |       Return_date       |       No_of_days       |       Status      |", fg="black")

    def view_cars():
        cars = customer_view_cars()
        text_area.delete('1.0', END)
        for car in cars:
            text_area.insert(END, f"{car}\n")
        label_message.config(text="|            Car_ID              |            Model            |        Year       |           License_Plate          |          Status          |       Rate_per_day       |", fg="black")

    # Red-bordered frame (c_frame1) at the top center
    c_frame1 = tk.Frame(master=root, relief="solid")
    c_frame1.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    button_view_cars = tk.Button(c_frame1, text="View Available Cars", command=view_cars)
    button_view_cars.pack(pady=10)
    button_view_bookings = tk.Button(c_frame1, text="View My Bookings", command=view_bookings)
    button_view_bookings.pack(pady=10)

    # Yellow and green labelled frames side by side
    centre_frame = tk.Frame(master=root)
    centre_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    c_frame2 = tk.LabelFrame(master=centre_frame, text='Rent car here')
    c_frame2.grid(row=0, column=0, padx=75, pady=10)
    label_car_id = tk.Label(c_frame2, text="Car ID (for rental)")
    label_car_id.pack(pady=5)
    entry_car_id = tk.Entry(c_frame2,borderwidth=2)
    entry_car_id.pack(pady=5,padx=15)

    label_no_of_days = tk.Label(c_frame2, text="Number of Days")
    label_no_of_days.pack(pady=5)
    entry_no_of_days = tk.Entry(c_frame2, borderwidth=2)
    entry_no_of_days.pack(pady=5,padx=15)

    button_rent_car = tk.Button(c_frame2, text="Rent Car", command=rent_car)
    button_rent_car.pack(pady=15)

    c_frame3 = tk.LabelFrame(master=centre_frame, text='Return car here')
    c_frame3.grid(row=0, column=1, padx=75, pady=10)
    label_rental_id = tk.Label(c_frame3, text="Rental ID (for return)")
    label_rental_id.pack(pady=5)
    entry_rental_id = tk.Entry(c_frame3, borderwidth=2)
    entry_rental_id.pack(pady=5,padx=15)

    button_return_car = tk.Button(c_frame3, text="Return Car", command=return_car)
    button_return_car.pack(pady=15)

    # Purple-bordered label below the labelled frames
    label_message = tk.Label(root, text="", borderwidth=1, relief="solid")
    label_message.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Text area at the bottom
    text_area = Text(root, height=10, width=85,borderwidth=2)
    text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()
