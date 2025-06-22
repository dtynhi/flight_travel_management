from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import and_

from app.extensions import db
from models.booking_model import TblTickets
from models.flight_model import Flight
from models.flight_ticket_class_model import FlightTicketClass

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/available-flights", methods=["GET"])
def get_available_flights():
    min_date = datetime.now() + timedelta(days=1)
    flights = db.session.query(Flight).join(FlightTicketClass).filter(
        and_(
            Flight.departure_time >= min_date,
            FlightTicketClass.available_seats > 0,
            Flight.status == "active"
        )
    ).all()

    results = []
    for flight in flights:
        results.append({
            "id": flight.id,
            "departure_time": flight.departure_time.strftime("%Y-%m-%d %H:%M"),
            "base_price": float(flight.base_price)
        })
    return jsonify(results)


@booking_bp.route("/book-ticket", methods=["POST"])
def book_ticket():
    data = request.json
    passenger_name = data.get("passenger_name")
    id_number = data.get("id_number")
    phone_number = data.get("phone_number")
    email = data.get("email")
    flight_id = data.get("flight_id")
    ticket_class_id = data.get("ticket_class_id")  # e.g., 1 for Hạng 1, 2 for Hạng 2

    # Tìm chuyến bay và lớp vé
    flight = Flight.query.get(flight_id)
    flight_class = FlightTicketClass.query.filter_by(flight_id=flight_id, ticket_class_id=ticket_class_id).first()

    if not flight or not flight_class or flight_class.available_seats <= 0:
        return jsonify({"error": "Không thể đặt vé"}), 400

    # Tạo vé
    new_ticket = TblTickets(
        passenger_name=passenger_name,
        ticket_class_id=ticket_class_id,
        flight_id=flight_id,
        seat_number="Chưa chỉ định",
        status="Đã đặt"
    )
    db.session.add(new_ticket)
    flight_class.available_seats -= 1
    db.session.commit()

    return jsonify({"message": "Đặt vé thành công", "ticket_price": float(flight_class.ticket_price)})
