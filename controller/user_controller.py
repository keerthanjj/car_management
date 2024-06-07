from flask import Blueprint, current_app, request, jsonify
from models import Booking, Car


user_bp = Blueprint('user', __name__)

@user_bp.route('/all_cars', methods=['GET'])
def get_cars():
    make = request.args.get('make')
    model = request.args.get('model')
    color=request.args.get('color')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_mileage = request.args.get('min_mileage', type=int)
    type_of_car = request.args.get('type_of_car')
    type_of_fuel = request.args.get('type_of_fuel')

    cars = Car.get_cars_by_criteria(
        make=make,
        model=model,
        color=color,
        min_price=min_price,
        max_price=max_price,
        min_mileage=min_mileage,
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
        vin = booking_details.get('vin')
        address = booking_details.get('address')
        
        # Validate required fields
        if not all([user_name, phone_number, vin, address]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Fetch car details from the Car model using VIN
        car = Car.get_by_vin(vin)
        
        # Check if car details are found
        if car:
            car_make = car.get('make')
            car_model = car.get('model')
            car_price = car.get('price')
            car_color = car.get('color')
        else:
            return jsonify({"error": "Car details not found"}), 404

        # Call create_booking method from Booking model
        booking_id = Booking.create_booking(user_name, phone_number, vin, car_make, car_model, car_color, car_price, address)
        
        if booking_id:
            return jsonify({"message": "Booking created successfully", "booking_id": booking_id}), 201
        else:
            return jsonify({"error": "Failed to create booking"}), 500
        
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500

