from app.extensions import db
from datetime import datetime

class FlightTicketClass(db.Model):
    __tablename__ = 'tbl_flight_ticket_classes'
    
    ticket_class_id = db.Column(db.Integer, db.ForeignKey('tbl_ticket_classes.id'), primary_key=True, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flights.id'), primary_key=True, nullable=False)
    total_seats = db.Column(db.Integer)
    available_seats = db.Column(db.Integer)
    ticket_price = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ticket_class = db.relationship('TicketClass', backref='flight_ticket_classes', lazy='select')
    flight = db.relationship('Flight', backref='flight_ticket_classes', lazy='select')

    def to_dict(self):
        """Convert flight ticket class to dictionary for API response"""
        return {
            'ticketClassId': self.ticket_class_id,
            'flightId': self.flight_id,
            'totalSeats': self.total_seats,
            'availableSeats': self.available_seats,
            'ticketPrice': float(self.ticket_price) if self.ticket_price else 0,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            # Include related data if loaded
            'ticketClass': self.ticket_class.to_dict() if self.ticket_class else None,
            'flight': self.flight.to_dict() if self.flight else None
        }

    def to_dict_minimal(self):
        """Convert to dictionary without relationship data for performance"""
        return {
            'ticketClassId': self.ticket_class_id,
            'flightId': self.flight_id,
            'totalSeats': self.total_seats,
            'availableSeats': self.available_seats,
            'ticketPrice': float(self.ticket_price) if self.ticket_price else 0,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<FlightTicketClass Flight:{self.flight_id} Class:{self.ticket_class_id}>'