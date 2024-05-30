from flask import Blueprint, request, jsonify
from models import Car

admin_bp = Blueprint('admin', __name__)


from flask import request, jsonify, render_template

# Import Car model and other necessary modules

@admin_bp.route('/add_car', methods=['POST'])
def add_car():
        car_data = request.json
        make = car_data.get("make")
        model = car_data.get("model")
        car_data_list = list(car_data.values())

        # Call the add_car method from the Car model
        Car.add_car(car_data_list)

        message = f"{make} {model} added successfully"
        return jsonify({"message": message}), 200
       

@admin_bp.route('/get_car', methods=['GET'])
def get_car():
    car_id = request.args.get('car_id')
    car = Car.get_by_id(car_id)
    if car:
        return jsonify(car), 200
    else:
        return jsonify({"message": "Car not found"}), 404

@admin_bp.route('/update_car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car_data = request.json
    # Convert dictionary to list
    car_data_list = [
        car_data['make'],
        car_data['model'],
        car_data['price'],
        car_data['year'],
        car_data['type_of_car'],
        car_data['type_of_fuel']
    ]
    Car.update_car(car_id, car_data_list)
    return jsonify({"message": "Car updated successfully"}), 200


@admin_bp.route('/delete_car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    Car.delete_car(car_id)
    return jsonify({"message": "Car deleted successfully"}), 200

@admin_bp.route('/all_cars', methods=['GET'])
def all_cars():
    cars = Car.get_all_cars()
    return jsonify({"cars": cars}), 200

@admin_bp.route('/current_bookings', methods=['GET'])
def current_bookings():
    bookings = Car.get_current_bookings()
    return jsonify({"bookings": bookings}), 200

