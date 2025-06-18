from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from models.booking_model import Booking

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/api/v1/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    try:
        booking = Booking(
            flight_name=data['flight_name'],
            price=float(data['price']),
            full_name=data['full_name'],
            phone=data['phone'],
            id_number=data['id_number'],
            email=data['email'],
            ticket_class=data['ticket_class'],
            departure_date=datetime.strptime(data['departure_date'], '%Y-%m-%d')
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': '✅ Booking created successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'❌ Error: {str(e)}'}), 400
