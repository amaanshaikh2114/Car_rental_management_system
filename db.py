import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amaan@2114",
        database="car_rental_db"
    )
