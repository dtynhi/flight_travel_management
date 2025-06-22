from models.tickets_model import Ticket
from models.monthly_report_model import MonthlyReport
from models.monthly_report_detail_model import MonthlyReportDetail
from models.yearly_report_model import YearlyReport
from models.flight_model import Flight
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import extract


class TicketService:

    @staticmethod
    def get_all_tickets():
        tickets = Ticket.query.filter_by(deletion_status='ACTIVE').all()
        return [t.to_dict() for t in tickets]

    @staticmethod
    def update_ticket(ticket_id, data):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError("Không tìm thấy vé")

        prev_status = ticket.status

        for key, value in data.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)

        # Nếu trạng thái mới là "Đã thanh toán", thì cập nhật báo cáo
        if prev_status != 'Đã thanh toán' and data.get('status') == 'Đã thanh toán':
            TicketService.update_report_after_ticket_paid(ticket)

        db.session.commit()
        return ticket.to_dict()

    @staticmethod
    def create_ticket(data):
        ticket = Ticket(
            ticket_class_id=data.get('ticket_class_id'),
            flight_id=data.get('flight_id'),
            status=data.get('status'),
            created_at=data.get('created_at', datetime.utcnow()),
            deletion_status='ACTIVE'
        )

        db.session.add(ticket)
        db.session.flush()  # để có ID nếu cần

        # Nếu ngay từ đầu trạng thái là "Đã thanh toán" thì cập nhật báo cáo
        if ticket.status == "Đã thanh toán":
            TicketService.update_report_after_ticket_paid(ticket)

        db.session.commit()
        return ticket.to_dict()

    @staticmethod
    def delete_ticket(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError("Không tìm thấy vé")

        ticket.deletion_status = 'deleted'
        db.session.commit()

    @staticmethod
    def update_report_after_ticket_paid(ticket):
        """Tự động cập nhật báo cáo khi vé được thanh toán"""
        flight = ticket.flight
        if not flight:
            raise ValueError("Không tìm thấy chuyến bay")

        departure_time = flight.departure_time or datetime.utcnow()
        month = departure_time.month
        year = departure_time.year
        price = float(flight.base_price or 0)

        # === BÁO CÁO THÁNG ===
        monthly_report = MonthlyReport.query.filter_by(month=month, year=year, deletion_status='ACTIVE').first()
        if not monthly_report:
            monthly_report = MonthlyReport(
                month=month,
                year=year,
                total_tickets_sold=0,
                total_revenue=0,
                created_at=datetime.utcnow(),
                deletion_status='ACTIVE'
            )
            db.session.add(monthly_report)
            db.session.flush()  # để lấy ID mới tạo

        monthly_report.total_tickets_sold += 1
        monthly_report.total_revenue += price

        # === CHI TIẾT BÁO CÁO THÁNG ===
        detail = MonthlyReportDetail.query.filter_by(
            report_id=monthly_report.id,
            flight_id=flight.id,
            deletion_status='ACTIVE'
        ).first()

        if not detail:
            detail = MonthlyReportDetail(
                report_id=monthly_report.id,
                flight_id=flight.id,
                tickets_sold=0,
                revenue=0,
                percentage=0,
                created_at=datetime.utcnow(),
                deletion_status='ACTIVE'
            )
            db.session.add(detail)

        detail.tickets_sold += 1
        detail.revenue += price

        # Cập nhật % đóng góp
        if monthly_report.total_revenue > 0:
            detail.percentage = round(detail.revenue / monthly_report.total_revenue, 2)

        # === BÁO CÁO NĂM ===
        yearly_report = YearlyReport.query.filter_by(year=year, month=month, deletion_status='ACTIVE').first()
        if not yearly_report:
            yearly_report = YearlyReport(
                year=year,
                month=month,
                number_of_flights=0,
                total_revenue=0,
                percentage=0,
                created_at=datetime.utcnow(),
                deletion_status='ACTIVE'
            )
            db.session.add(yearly_report)

        yearly_report.total_revenue += price
        yearly_report.number_of_flights = Flight.query.filter(
            extract('month', Flight.departure_time) == month,
            extract('year', Flight.departure_time) == year,
            Flight.status != 'Đã hủy',  # hoặc tùy theo enum/chuỗi của bạn
            Flight.deletion_status == 'ACTIVE'
        ).count()

        # Tính tổng doanh thu năm để cập nhật phần trăm
        total_yearly_revenue = db.session.query(db.func.sum(YearlyReport.total_revenue)).filter_by(
            year=year, deletion_status='ACTIVE'
        ).scalar() or 1  # tránh chia 0

        yearly_report.percentage = round(yearly_report.total_revenue / total_yearly_revenue, 2)

        db.session.commit()
