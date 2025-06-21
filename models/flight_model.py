from app.extensions import db
from datetime import datetime

class Flight(db.Model):
    __tablename__ = 'tbl_flights'
    
    id = db.Column(db.Integer, primary_key=True)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('tbl_airports.id'), nullable=False)  # ✅ Added FK
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('tbl_airports.id'), nullable=False)    # ✅ Added FK
    departure_time = db.Column(db.DateTime, nullable=False)
    flight_duration = db.Column(db.Integer)  # integer (minutes)
    base_price = db.Column(db.Numeric(15, 0))  # numeric(15,0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # ✅ Fixed datetime
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Fixed datetime
    status = db.Column(db.String(20))  # character varying(20)
    arrival_time = db.Column(db.DateTime, nullable=False)

    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id], 
                                      backref='departing_flights', lazy='select')
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id],
                                    backref='arriving_flights', lazy='select')

    def to_dict(self):
        """Convert flight to dictionary for API response"""
        duration_str = self._format_duration(self.flight_duration) if self.flight_duration else "N/A"
        
        return {
            'id': self.id,
            'flightCode': f"FL{self.id:04d}",  # Generate flight code from ID
            'departureAirportId': self.departure_airport_id,
            'arrivalAirportId': self.arrival_airport_id,
            'departureAirport': self.departure_airport.airport_name if self.departure_airport else f"Airport {self.departure_airport_id}",
            'arrivalAirport': self.arrival_airport.airport_name if self.arrival_airport else f"Airport {self.arrival_airport_id}",
            'departureTime': self.departure_time.isoformat() if self.departure_time else None,
            'arrivalTime': self.arrival_time.isoformat() if self.arrival_time else None,
            'flightDuration': duration_str,
            'basePrice': float(self.base_price) if self.base_price else 0,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

    def _format_duration(self, minutes):
        """Convert minutes to 'Xh Ym' format"""
        if not minutes:
            return "N/A"
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"
        return f"{mins}m"

    def __repr__(self):
        return f'<Flight {self.id}: {self.departure_airport_id} -> {self.arrival_airport_id}>'