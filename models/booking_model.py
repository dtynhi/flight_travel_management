from app.extensions import db
from datetime import datetime, timezone

# Chỉ khai báo bảng TblTickets ở đây, các bảng khác sẽ import từ file riêng

class TblTickets(db.Model):
    __tablename__ = 'tbl_tickets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(255), nullable=False)
    ticket_class_id = db.Column(db.Integer, db.ForeignKey('tbl_flight_ticket_classes.ticket_class_id'), nullable=False)
    seat_number = db.Column(db.String(50), default="Chưa chỉ định")
    status = db.Column(db.String(50), default="Đã đặt")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
