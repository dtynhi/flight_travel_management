from app.extensions import db
from datetime import datetime, timedelta
from constant.constant import Status
from models.airport_model import Airport

class Flight(db.Model):
    __tablename__ = 'tbl_flights'

    id = db.Column(db.Integer, primary_key=True)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('tbl_airports.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('tbl_airports.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    flight_duration = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=Status.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id])
    ticket_classes = db.relationship('FlightTicketClass', backref='flight', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "from_airport_id": self.departure_airport_id,
            "from_airport": self.departure_airport.airport_name if self.departure_airport else None,
            "to_airport_id": self.arrival_airport_id,
            "to_airport": self.arrival_airport.airport_name if self.arrival_airport else None,
            "departure_time": self.departure_time.isoformat(),
            "arrival_time": self.arrival_time.isoformat(),
            "flight_duration": self.flight_duration,
            "base_price": float(self.base_price),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }



