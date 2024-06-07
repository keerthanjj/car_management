import datetime
from flask import current_app
import snowflake.connector
from config import SNOWFLAKE
from datetime import datetime 

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
        query = ("INSERT INTO car_management.public.car (vin, make, model,color, price, mileage_in_km, year, type_of_car, type_of_fuel, status) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        # Execute the INSERT query
        Car.execute_query(query, car_data)
        
        # Fetch the VIN using the inserted VIN
        select_query = (
            "SELECT vin FROM car_management.public.car "
            "WHERE vin = %s"
        )
        result = Car.execute_query(select_query, (car_data[0],), fetchall=False)
        vin = result[0] if result else None
        
        return vin
        

    @staticmethod
    def update_car(vin, car_data):
        query = ("UPDATE car_management.public.car SET make = %s, model = %s, color = %s, price = %s, "
                "mileage_in_km = %s, year = %s, type_of_car = %s, type_of_fuel = %s "
                "WHERE vin = %s")
        # Pass vin as a separate parameter
        car_data.append(vin)
        Car.execute_query(query, car_data)

        

    @staticmethod
    def delete_car(vin):
        query = "DELETE FROM car WHERE vin = %s"
        Car.execute_query(query, (vin,))


    @staticmethod
    def get_all_cars():
        query = "SELECT * FROM car"
        return Car.execute_query(query, fetchall=True)

    @staticmethod
    def get_current_bookings():
        query = "SELECT * FROM bookings"
        return Car.execute_query(query, fetchall=True)
    
    @staticmethod
    def get_cars_by_criteria(make=None, model=None, color=None,min_price=None, max_price=None, min_mileage=None, type_of_car=None, type_of_fuel=None):
        query = "SELECT * FROM car WHERE status = 'available'"
        data = []

        if make:
            query += " AND make = %s"
            data.append(make)
        if model:
            query += " AND model = %s"
            data.append(model)
        if color:
            query+="AND color =%s"
            data.append(color)
        if min_price:
            query += " AND price >= %s"
            data.append(min_price)
        if max_price:
            query += " AND price <= %s"
            data.append(max_price)
        if min_mileage:
            query += " AND mileage_in_km >= %s"
            data.append(min_mileage)
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
    def get_by_vin(vin):
        query = "SELECT make, model, color, price, mileage_in_km, year, type_of_car, type_of_fuel, status FROM car_management.public.car WHERE vin = %s"
        try:
            result = Car.execute_query(query, (vin,), fetchall=False)
            if result:
                make, model,color, price, mileage_in_km, year, type_of_car, type_of_fuel, status = result
                current_app.logger.info(f"Car details found: make={make}, model={model}, vin={vin}")
                return {
                    'make': make,
                    'model': model,
                    'color':color,
                    'price': price,
                    'mileage_in_km': mileage_in_km,
                    'year': year,
                    'type_of_car': type_of_car,
                    'type_of_fuel': type_of_fuel,
                    'status': status
                }
            else:
                current_app.logger.error(f"No car details found for vin: {vin}")
                return None
        except Exception as e:
            current_app.logger.error(f"Database query failed: {e}")
            return None



        

class Booking:
    @staticmethod
    def create_booking(user_name, phone_number, vin, car_make, car_model, car_color, price, address):
        # Validate input parameters
        if not (user_name and phone_number and vin and car_make and car_model and car_color and price and address):
            current_app.logger.error("Missing booking details")
            return None

        # Generate booking date
        booking_date = datetime.utcnow()

        insert_query = """
            INSERT INTO car_management.public.bookings 
            (user_name, phone_number, vin, make, model, color, price, booking_date, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (user_name, phone_number, vin, car_make, car_model, car_color, price, booking_date, address)

        try:
            # Execute the insert query
            current_app.logger.info(f"Executing insert query with data: {data}")
            Car.execute_query(insert_query, data, fetchall=False)

            # Retrieve the booking_id based on the inserted data
            select_query = """
                SELECT ID
                FROM car_management.public.bookings
                WHERE user_name = %s AND phone_number = %s AND vin = %s AND make = %s 
                AND model = %s AND color = %s AND price = %s AND booking_date = %s AND address = %s
                ORDER BY ID DESC
                LIMIT 1
            """
            result = Car.execute_query(select_query, data, fetchall=True)
            current_app.logger.info(f"Query executed, result: {result}")

            if result and len(result) > 0:
                booking_id = result[0][0]
                current_app.logger.info(f"Booking created successfully with ID: {booking_id}")

                # Update car status to booked
                update_query = """
                    UPDATE car_management.public.car
                    SET status = 'Booked'
                    WHERE vin = %s
                """
                Car.execute_query(update_query, (vin,), fetchall=False)
                current_app.logger.info(f"Car status updated to 'Booked' for VIN: {vin}")

                return booking_id
            else:
                current_app.logger.error("No result returned from the select query")
                return None
        except Exception as e:
            current_app.logger.error(f"Database query failed: {e}")
            return None
