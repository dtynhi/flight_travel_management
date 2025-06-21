from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import and_
from app import db
from models.booking_model import TblFlights, TblFlightTicketClasses, TblTickets

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/available-flights", methods=["GET"])
def get_available_flights():
    min_date = datetime.now() + timedelta(days=1)
    flights = db.session.query(TblFlights).join(TblFlightTicketClasses).filter(
        and_(
            TblFlights.departure_time >= min_date,
            TblFlightTicketClasses.available_seats > 0,
            TblFlights.status == True
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
    passenger_name = data["passenger_name"]
    id_number = data["id_number"]
    phone_number = data["phone_number"]
    email = data["email"]
    flight_id = data["flight_id"]
    ticket_class = data["ticket_class"]  # "Hạng 1" or "Hạng 2"

    # Tìm flight và lớp vé
    flight = TblFlights.query.get(flight_id)
    flight_class = TblFlightTicketClasses.query.filter_by(flight_id=flight_id).first()

    if not flight or not flight_class or flight_class.available_seats <= 0:
        return jsonify({"error": "Không thể đặt vé"}), 400

    # Tính giá
    if ticket_class == "Hạng 1":
        ticket_price = float(flight.base_price) * 1.05
    else:
        ticket_price = float(flight.base_price)

    # Tạo vé
    new_ticket = TblTickets(
        passenger_name=passenger_name,
        ticket_class_id=flight_class.id,
        seat_number="Chưa chỉ định",
        status="Đã đặt",
    )
    db.session.add(new_ticket)
    flight_class.available_seats -= 1
    db.session.commit()

    return jsonify({"message": "Đặt vé thành công", "ticket_price": ticket_price})
