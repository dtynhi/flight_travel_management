from app.extensions import db
from datetime import datetime
from models.ticket_model import Ticket
from models.flight_model import Flight
from models.flight_ticket_class_model import FlightTicketClass
from models.monthly_report_model import MonthlyReport
from models.monthly_report_detail_model import MonthlyReportDetail
from models.yearly_report_model import YearlyReport
from sqlalchemy import extract


class TicketService:
    @staticmethod
    def book_ticket(data):
        passenger_name = data.get("passenger_name")
        id_number = data.get("id_number")
        phone_number = data.get("phone_number")
        email = data.get("email")
        flight_id = data.get("flight_id")
        ticket_class_id = data.get("ticket_class_id")

        flight = Flight.query.get(flight_id)
        flight_class = FlightTicketClass.query.filter_by(
            flight_id=flight_id, ticket_class_id=ticket_class_id
        ).first()

        if not flight or not flight_class or flight_class.available_seats <= 0:
            raise ValueError("Không thể đặt vé")

        new_ticket = Ticket(
            flight_id=flight_id, ticket_class_id=ticket_class_id, status="Đã xác nhận"
        )

        db.session.add(new_ticket)
        flight_class.available_seats -= 1
        db.session.commit()

        TicketService.update_report_after_ticket_paid(new_ticket)

        return new_ticket

    @staticmethod
    def update_report_after_ticket_paid(ticket):
        """Tự động cập nhật báo cáo khi vé được thanh toán"""

        if ticket.status not in ["Đã thanh toán", "Đã xác nhận", "BOOKED"]:
            return
        flight = Flight.query.get(ticket.flight_id)
        if not flight:
            raise ValueError("Không tìm thấy chuyến bay")

        departure_time = flight.departure_time or datetime.utcnow()
        month = departure_time.month
        year = departure_time.year
        price = float(flight.base_price or 0)

        # === BÁO CÁO THÁNG ===
        monthly_report = MonthlyReport.query.filter_by(
            month=month, year=year, deletion_status="ACTIVE"
        ).first()
        if not monthly_report:
            monthly_report = MonthlyReport(
                month=month,
                year=year,
                total_tickets_sold=0,
                total_revenue=0,
                created_at=datetime.utcnow(),
                deletion_status="ACTIVE",
            )
            db.session.add(monthly_report)
            db.session.flush()

        monthly_report.total_tickets_sold += 1
        monthly_report.total_revenue += price

        # === CHI TIẾT BÁO CÁO THÁNG ===
        detail = MonthlyReportDetail.query.filter_by(
            report_id=monthly_report.id, flight_id=flight.id, deletion_status="ACTIVE"
        ).first()

        if not detail:
            detail = MonthlyReportDetail(
                report_id=monthly_report.id,
                flight_id=flight.id,
                tickets_sold=0,
                revenue=0,
                percentage=0,
                created_at=datetime.utcnow(),
                deletion_status="ACTIVE",
            )
            db.session.add(detail)

        detail.tickets_sold += 1
        detail.revenue += price

        if monthly_report.total_revenue > 0:
            detail.percentage = round(detail.revenue / monthly_report.total_revenue, 2)

        # === BÁO CÁO NĂM ===
        yearly_report = YearlyReport.query.filter_by(
            year=year, month=month, deletion_status="ACTIVE"
        ).first()
        if not yearly_report:
            yearly_report = YearlyReport(
                year=year,
                month=month,
                number_of_flights=0,
                total_revenue=0,
                percentage=0,
                created_at=datetime.utcnow(),
                deletion_status="ACTIVE",
            )
            db.session.add(yearly_report)

        yearly_report.total_revenue += price
        yearly_report.number_of_flights = Flight.query.filter(
            extract("month", Flight.departure_time) == month,
            extract("year", Flight.departure_time) == year,
            Flight.status != "Đã hủy",
        ).count()

        total_yearly_revenue = (
            db.session.query(db.func.sum(YearlyReport.total_revenue))
            .filter_by(year=year, deletion_status="ACTIVE")
            .scalar()
            or 1
        )

        yearly_report.percentage = round(
            yearly_report.total_revenue / total_yearly_revenue, 2
        )

        db.session.commit()
