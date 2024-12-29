import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_database_password",
        database="your_database_name"        # in my case it's car_rental_db
    )
