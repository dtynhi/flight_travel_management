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
    """Lấy danh sách chuyến bay còn vé từ ngày mai trở đi (không dùng timezone)"""
    try:
        now = datetime.now()
        min_date = now + timedelta(days=1)
        flights = (
            db.session.query(Flight)
            .join(FlightTicketClass)
            .filter(
                Flight.departure_time >= min_date,
                Flight.status == "ACTIVE",
                FlightTicketClass.available_seats > 0,
            )
            .distinct()
            .all()
        )
        print(f"[DEBUG] Số chuyến bay còn ghế và status 'ACTIVE': {len(flights)}")
        print(
            f"[DEBUG] ID các chuyến bay còn ghế và status 'ACTIVE': {[f.id for f in flights]}"
        )

        results = []
        for flight in flights:
            results.append(
                {
                    "id": flight.id,
                    "departure_time": flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                    "base_price": float(
                        flight.base_price
                    ),
                }
            )

        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ticket_bp.route("/book", methods=["POST"])
def book_ticket():
    """Đặt vé máy bay và ghi nhận doanh thu"""
    try:
        data = request.get_json()
        passenger_name = data.get("passenger_name")
        if not passenger_name:
            return jsonify({"error": "Thiếu thông tin tên hành khách"}), 400

        ticket = TicketService.book_ticket(data)
        return (
            jsonify(
                {
                    "passenger_name": passenger_name,
                    "ticket_id": ticket.id,
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
    except Exception as e:
        return jsonify({"error": str(e)}), 400
