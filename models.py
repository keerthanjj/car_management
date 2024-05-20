import datetime
from flask import current_app
import snowflake.connector
from config import SNOWFLAKE

class Car:
    @staticmethod
    def execute_query(query, params=None, fetchall=True):
        try:
            connection = snowflake.connector.connect(**SNOWFLAKE)  # Define your method to get a DB connection
            cursor = connection.cursor()
            current_app.logger.info(f"Executing query: {query} with params: {params}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetchall:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            
            current_app.logger.info(f"Query result: {result}")
            cursor.close()
            connection.close()
            return result
        except Exception as e:
            current_app.logger.error(f"Database query failed: {e}")
            return None
    
    
   

    @staticmethod
    def add_car(car_data):
        query = ("INSERT INTO car_management.public.car ( make, model, price, year, type_of_car, type_of_fuel) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        return Car.execute_query(query, car_data)

    @staticmethod
    def update_car(car_id, car_data):
        query = ("UPDATE car SET make = %s, model = %s, price = %s, "
                 "year = %s, type_of_car = %s, type_of_fuel = %s "
                 "WHERE id = %s")
        car_data.append(car_id)
        Car.execute_query(query, car_data)

    @staticmethod
    def delete_car(car_id):
        query = "DELETE FROM car WHERE id = %s"
        Car.execute_query(query, (car_id,))

    @staticmethod
    def get_all_cars():
        query = "SELECT * FROM car"
        return Car.execute_query(query, fetchall=True)

    @staticmethod
    def get_current_bookings():
        query = "SELECT * FROM booking"
        return Car.execute_query(query, fetchall=True)
    
    @staticmethod
    def get_cars_by_criteria(make=None, model=None, min_price=None, max_price=None, type_of_car=None, type_of_fuel=None):
        query = "SELECT * FROM car_management.public.car WHERE 1=1"
        data = []

        if make:
            query += " AND make = %s"
            data.append(make)
        if model:
            query += " AND model = %s"
            data.append(model)
        if min_price:
            query += " AND price >= %s"
            data.append(min_price)
        if max_price:
            query += " AND price <= %s"
            data.append(max_price)
        if type_of_car:
            query += " AND type_of_car = %s"
            data.append(type_of_car)
        if type_of_fuel:
            query += " AND type_of_fuel = %s"
            data.append(type_of_fuel)

        # Log the query and data
        current_app.logger.debug(f"Query: {query}")
        current_app.logger.debug(f"Data: {data}")

        return Car.execute_query(query, tuple(data), fetchall=True)
    
    @staticmethod
    def get_by_id(car_id):
        query = "SELECT make, model FROM car_management.public.car WHERE car_id = %s"
        try:
            result = Car.execute_query(query, (car_id,), fetchall=False)
            if result:
                make, model = result
                current_app.logger.info(f"Car details found: make={make}, model={model}")
                return {'make': make, 'model': model}
            else:
                current_app.logger.error(f"No car details found for car_id: {car_id}")
                return None
        except Exception as e:
            current_app.logger.error(f"Database query failed: {e}")
            return None


        

class Booking:
    @staticmethod
    def create_booking(user_name, phone_number, car_id, car_make, car_model, booking_date, address):
        query = """
            INSERT INTO car_management.public.bookings 
            (user_name, phone_number, car_id, car_make, car_model, booking_date, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING booking_id
        """
        data = (user_name, phone_number, car_id, car_make, car_model, booking_date, address)
        
        try:
            current_app.logger.info(f"Executing insert query with data: {data}")
            result = Car.execute_query(query, data, fetchall=False)
            if result:
                booking_id = result[0]
                current_app.logger.info(f"Booking created successfully with ID: {booking_id}")
                return booking_id
            else:
                current_app.logger.error("No result returned from the insert query")
                return None
        except Exception as e:
            current_app.logger.error(f"Database query failed: {e}")
            return None



