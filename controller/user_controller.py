from flask import Blueprint, current_app, request, jsonify
from models import Booking, Car


user_bp = Blueprint('user', __name__)

@user_bp.route('/all_cars', methods=['GET'])
def get_cars():
    make = request.args.get('make')
    model = request.args.get('model')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    type_of_car = request.args.get('type_of_car')
    type_of_fuel = request.args.get('type_of_fuel')

    cars = Car.get_cars_by_criteria(
        make=make,
        model=model,
        min_price=min_price,
        max_price=max_price,
        type_of_car=type_of_car,
        type_of_fuel=type_of_fuel
    )

    if not cars:
        return jsonify({"message": "No cars found matching the criteria"}), 404

    return jsonify({"cars": cars}), 200


@user_bp.route('/book_car', methods=['POST'])
def create_booking():
    """
    Endpoint to create a new booking.
    """
    try:
        # Extract booking details from the request JSON
        booking_details = request.get_json()
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
            car_price = car.get('price')
        else:
            return jsonify({"error": "Car details not found"}), 404

        # Call create_booking method from Booking model
        booking_id = Booking.create_booking(user_name, phone_number, car_id, car_make, car_model, car_price, address)
        
        if booking_id:
            return jsonify({"message": "Booking created successfully", "booking_id": booking_id}), 201
        else:
            return jsonify({"error": "Failed to create booking"}), 500
        
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500
