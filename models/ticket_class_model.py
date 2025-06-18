from app.extensions import db
from datetime import datetime
from constant.constant import Status

class TicketClass(db.Model):
    __tablename__ = 'tbl_ticket_classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)  # e.g., Economy, Business, First Class
    price_multiplier = db.Column(db.Numeric(6, 2), nullable=False)  # e.g., 1.00, 1.50, etc.
    status = db.Column(db.String(20), nullable=False, default=Status.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "price_multiplier": float(self.price_multiplier),
            "status": self.status
        }

