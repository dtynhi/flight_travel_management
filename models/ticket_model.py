# models/ticket_model.py
from app.extensions import db
from datetime import datetime, timezone


class Ticket(db.Model):
    __tablename__ = "tbl_tickets"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    ticket_class_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_flight_ticket_classes.ticket_class_id"),
        nullable=False,
    )
    flight_id = db.Column(db.Integer, db.ForeignKey("tbl_flights.id"), nullable=False)
    status = db.Column(db.String(50), default="Đã xác nhận")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_class_id": self.ticket_class_id,
            "flight_id": self.flight_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
