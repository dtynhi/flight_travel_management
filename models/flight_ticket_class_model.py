from app.extensions import db
from datetime import datetime

class FlightTicketClass(db.Model):
    __tablename__ = 'tbl_flight_ticket_classes'

    ticket_class_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flights.id'), primary_key=True)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "ticket_class_id": self.ticket_class_id,
            "flight_id": self.flight_id,
            "total_seats": self.total_seats,
            "available_seats": self.available_seats,
            "ticket_price": float(self.ticket_price),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

