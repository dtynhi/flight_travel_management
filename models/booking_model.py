from app import db
from datetime import datetime

class TblFlights(db.Model):
    __tablename__ = 'tbl_flights'

    id = db.Column(db.Integer, primary_key=True)
    departure_airport_id = db.Column(db.Integer, nullable=False)
    arrival_airport_id = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    flight_duration = db.Column(db.Integer, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    base_price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ticket_classes = db.relationship('TblFlightTicketClasses', backref='flight', lazy=True)


class TblFlightTicketClasses(db.Model):
    __tablename__ = 'tbl_flight_ticket_classes'

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flights.id'), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tickets = db.relationship('TblTickets', backref='ticket_class', lazy=True)


class TblTickets(db.Model):
    __tablename__ = 'tbl_tickets'

    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(255), nullable=False)
    ticket_class_id = db.Column(db.Integer, db.ForeignKey('tbl_flight_ticket_classes.id'), nullable=False)
    seat_number = db.Column(db.String(50), default="Chưa chỉ định")
    status = db.Column(db.String(50), default="Đã đặt")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
