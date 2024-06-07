import uuid
from flask import Blueprint, request, jsonify
from models import Car

admin_bp = Blueprint('admin', __name__)


# Import Car model and other necessary modules

@admin_bp.route('/add_car', methods=['POST'])
def add_car():
    car_data = request.json
    make = car_data.get("make")
    model = car_data.get("model")
    color = car_data.get("color")
    price = car_data.get("price")
    mileage_in_km = car_data.get("mileage_in_km", 0)
    year = car_data.get("year")
    type_of_car = car_data.get("type_of_car")
    type_of_fuel = car_data.get("type_of_fuel")
    status = car_data.get("status", "available")

    # Generate a 4-digit random number for VIN
    vin = str(uuid.uuid4().int)[:4]

    car_data_list = [
        vin, make, model,color, price, mileage_in_km, year, type_of_car, type_of_fuel, status
    ]

    # Call the add_car method from the Car model and get the VIN
    car_id = Car.add_car(car_data_list)

    message = f"{make} {model} added successfully with VIN {vin}"
    return jsonify({"message": message, "vin": vin}), 200

       

@admin_bp.route('/get_car', methods=['GET'])
def get_car():
    vin = request.args.get('vin')
    car = Car.get_by_vin(vin)
    if car:
        return jsonify(car), 200
    else:
        return jsonify({"message": "Car not found"}), 404


@admin_bp.route('/update_car', methods=['PUT'])
def update_car():
    vin = request.args.get('vin')
    car_data = request.json
    # Convert dictionary to list and include mileage_in_km
    car_data_list = [
        car_data['make'],
        car_data['model'],
        car_data['color'],  # Corrected position of color
        car_data['price'],  # Corrected position of price
        car_data['mileage_in_km'],
        car_data['year'],
        car_data['type_of_car'],
        car_data['type_of_fuel']
    ]
    Car.update_car(vin, car_data_list)
    return jsonify({"message": "Car updated successfully"}), 200




@admin_bp.route('/delete_car/<string:vin>', methods=['DELETE'])
def delete_car(vin):
    Car.delete_car(vin)
    return jsonify({"message": "Car deleted successfully"}), 200


@admin_bp.route('/all_cars', methods=['GET'])
def all_cars():
    cars = Car.get_all_cars()
    return jsonify({"cars": cars}), 200

@admin_bp.route('/current_bookings', methods=['GET'])
def current_bookings():
    bookings = Car.get_current_bookings()
    return jsonify({"bookings": bookings}), 200

