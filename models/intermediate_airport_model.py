from app.extensions import db
from datetime import datetime

class IntermediateAirport(db.Model):
    __tablename__ = 'tbl_intermediate_airports'

    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flights.id'), primary_key=True)
    intermediate_airport_id = db.Column(db.Integer, db.ForeignKey('tbl_airports.id'), primary_key=True)
    stop_order = db.Column(db.Integer, nullable=False)
    stop_duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "flight_id": self.flight_id,
            "intermediate_airport_id": self.intermediate_airport_id,
            "stop_order": self.stop_order,
            "stop_duration": self.stop_duration,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


