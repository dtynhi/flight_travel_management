from models.ticket_model import Ticket
from models.monthly_report_model import MonthlyReport
from models.monthly_report_detail_model import MonthlyReportDetail
from models.yearly_report_model import YearlyReport
from models.flight_model import Flight
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import extract
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models.flight_ticket_class_model import FlightTicketClass
from sqlalchemy import and_, or_, func


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
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ticket_bp.route("/book", methods=["POST"])
def book_ticket():
    """Đặt vé máy bay"""
    try:
        data = request.get_json()

        required_fields = ["flight_id", "ticket_class_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Thiếu thông tin: {field}"}), 400

        # passenger_name = data.get("passenger_name")  # Bỏ dòng này
        email = data.get("email")
        flight_id = data["flight_id"]
        ticket_class_id = data["ticket_class_id"]

        # Kiểm tra chuyến bay có tồn tại và còn hoạt động không
        flight = (
            db.session.query(Flight).filter_by(id=flight_id, status="ACTIVE").first()
        )
        if not flight:
            return jsonify({"error": "Chuyến bay không hợp lệ hoặc đã huỷ"}), 404

        # Kiểm tra hạng vé có tồn tại không
        ticket_class = (
            db.session.query(FlightTicketClass)
            .filter_by(flight_id=flight_id, ticket_class_id=ticket_class_id)
            .first()
        )
        if not ticket_class:
            return jsonify({"error": "Hạng vé không hợp lệ"}), 404

        if ticket_class.available_seats <= 0:
            return jsonify({"error": "Hạng vé đã hết chỗ"}), 400

        # Tạo vé mới
        ticket = Ticket(
            flight_id=flight_id,
            ticket_class_id=ticket_class_id,
            status="BOOKED",
            # seat_number="Chưa chỉ định",  # Bỏ nếu không có trong DB
            # booking_time=datetime.utcnow(),
        )

        # Trừ số ghế còn lại
        ticket_class.available_seats -= 1

        db.session.add(ticket)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Đặt vé thành công",
                    "ticket_id": ticket.id,
                    "available_seats": ticket_class.available_seats,
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Lỗi cơ sở dữ liệu: " + str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống: " + str(e)}), 500


@ticket_bp.route("/my", methods=["GET"])
def get_my_tickets():
    """(Dự phòng) Trả danh sách vé của người dùng nếu có auth"""
    try:
        user_email = request.args.get("email")
        if not user_email:
            return jsonify({"error": "Thiếu thông tin email"}), 400

        tickets = (
            TblTickets.query.join(Flight).filter(TblTickets.email == user_email).all()
        )

        result = []
        for t in tickets:
            result.append(
                {
                    "ticket_id": t.id,
                    # "passenger_name": t.passenger_name,  # Bỏ nếu không có trong DB
                    "flight_id": t.flight_id,
                    "ticket_class_id": t.ticket_class_id,
                    # "seat_number": t.seat_number,  # Bỏ nếu không có trong DB
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
        return jsonify({"error": "Không thể lấy danh sách vé: " + str(e)}), 500
        return jsonify({"error": "Không thể lấy danh sách vé: " + str(e)}), 500
