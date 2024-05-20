from flask import Blueprint, current_app, request, jsonify
from models import Booking, Car


from datetime import datetime


user_bp = Blueprint('user', __name__)

@user_bp.route('/cars', methods=['POST'])
def get_cars():
    """
    Endpoint to get cars based on user selection criteria.
    """
    criteria = request.json

    # Extract criteria from JSON data
    make = criteria.get('make')
    model = criteria.get('model')
    min_price = criteria.get('min_price')
    max_price = criteria.get('max_price')
    type_of_car = criteria.get('type_of_car')
    type_of_fuel = criteria.get('type_of_fuel')

    # Call method to retrieve cars based on criteria
    cars = Car.get_cars_by_criteria(make=make, model=model, min_price=min_price, max_price=max_price, type_of_car=type_of_car, type_of_fuel=type_of_fuel)

    # Return list of cars as JSON response
    return jsonify({"cars": cars}), 200


@user_bp.route('/book_car', methods=['POST'])
def create_booking():
    """
    Endpoint to create a new booking.
    """
    try:
        # Extract booking details from the request JSON
        booking_details = request.json
        user_name = booking_details.get('user_name')
        phone_number = booking_details.get('phone_number')
        car_id = booking_details.get('car_id')
        address = booking_details.get('address')
        
        # Validate required fields
        if not all([user_name, phone_number, car_id, address]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Fetch car details from the Car model using car_id
        car = Car.get_by_id(car_id)
        
        # Check if car details are found
        if car:
            car_make = car.get('make')
            car_model = car.get('model')
        else:
            return jsonify({"error": "Car details not found"}), 404

        # Capture current date and time
        booking_date = datetime.now()

        # Call create_booking method from Booking model
        booking_id = Booking.create_booking(user_name, phone_number, car_id, car_make, car_model, booking_date, address)
        
        if booking_id:
            return jsonify({"message": "Booking created successfully", "booking_id": booking_id}), 201
        else:
            return jsonify({"error": "Failed to create booking"}), 500
        
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500


