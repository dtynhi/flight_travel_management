from models.ticket_model import Ticket
from models.flight_model import Flight
from models.flight_ticket_class_model import FlightTicketClass
from app.extensions import db
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import and_
from services.app.ticket_service import TicketService

ticket_bp = Blueprint("ticket", __name__, url_prefix="/api/v1/tickets")


@ticket_bp.route("/available-flights", methods=["GET"])
def get_available_flights():
    """Lấy danh sách chuyến bay còn vé từ ngày mai trở đi"""
    try:
        min_date = datetime.now() + timedelta(days=1)
        flights = (
            db.session.query(Flight)
            .join(FlightTicketClass)
            .filter(
                and_(
                    Flight.departure_time >= min_date,
                    FlightTicketClass.available_seats > 0,
                    Flight.status == "ACTIVE",
                )
            )
            .distinct()
            .all()
        )
        results = []
        for flight in flights:
            results.append(
                {
                    "id": flight.id,
                    "departure_time": flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                    "base_price": float(flight.base_price),
                }
            )
        # Nếu không có chuyến bay nào, trả về mảng rỗng
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ticket_bp.route("/book", methods=["POST"])
def book_ticket():
    """Đặt vé máy bay và ghi nhận doanh thu"""
    try:
        data = request.get_json()
        # Lấy passenger_name từ request
        passenger_name = data.get("passenger_name")
        ticket = TicketService.book_ticket(data)
        return (
            jsonify(
                {
                    "message": "Đặt vé thành công",
                    "ticket_id": ticket.id,
                    "passenger_name": passenger_name,  # Trả về passenger_name
                    "flight_id": ticket.flight_id,
                    "ticket_class_id": ticket.ticket_class_id,
                    "status": ticket.status,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ticket_bp.route("/my", methods=["GET"])
def get_my_tickets():
    """Trả danh sách vé theo email"""
    try:
        user_email = request.args.get("email")
        if not user_email:
            return jsonify({"error": "Thiếu thông tin email"}), 400

        tickets = Ticket.query.join(Flight).filter(Ticket.email == user_email).all()

        result = []
        for t in tickets:
            result.append(
                {
                    "ticket_id": t.id,
                    "flight_id": t.flight_id,
                    "ticket_class_id": t.ticket_class_id,
                    "status": t.status,
                    "departure_time": (
                        t.flight.departure_time.strftime("%Y-%m-%d %H:%M")
                        if t.flight
                        else None
                    ),
                }
            )

        return jsonify({"data": result}), 200
    except Exception as e:
        return jsonify({"error": "Không thể lấy danh sách vé: " + str(e)}), 500
