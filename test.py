from models import Car,Booking
from models import Booking  # Import your Flask app
user_name = "John Doe"
phone_number = "1234567890"
car_id = 1
car_make = "Toyota"
car_model = "Camry"
booking_date = "2024-05-20"
address = "123 Main St"

with Booking.app_context():
    booking_id = Car.create_booking(user_name, phone_number, car_id, car_make, car_model, booking_date, address)
    if booking_id:
        print(f"Booking ID: {booking_id}")
    else:
        print("Booking creation failed")



