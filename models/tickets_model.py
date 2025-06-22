from app.extensions import db
from datetime import datetime, timezone

class Ticket(db.Model):
    __tablename__ = 'tbl_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_class_id = db.Column(db.Integer, db.ForeignKey('tbl_ticket_classes.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('tbl_flights.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Ví dụ: Pending, Paid, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deletion_status = db.Column(db.String(20), default='active')

    # Relationships
    ticket_class = db.relationship('TicketClass', backref='tickets', lazy='select')
    flight = db.relationship('Flight', backref='tickets', lazy='select')

    def to_dict(self):
        return {
            'id': self.id,
            'ticketClassId': self.ticket_class_id,
            'flightId': self.flight_id,
            'status': self.status,
            'deletionStatus': self.deletion_status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'ticketClass': self.ticket_class.to_dict() if self.ticket_class else None,
            'flight': self.flight.to_dict() if self.flight else None
        }

    def __repr__(self):
        return f'<Ticket {self.id} - Flight: {self.flight_id} | Class: {self.ticket_class_id}>'
