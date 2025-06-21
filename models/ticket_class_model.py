from app.extensions import db
from datetime import datetime, timezone

class TicketClass(db.Model):
    __tablename__ = 'tbl_ticket_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(20), nullable=False)
    price_multiplier = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    status = db.Column(db.String(20))

    def to_dict(self):
        """Convert ticket class to dictionary for API response"""
        return {
            'id': self.id,
            'className': self.class_name,
            'priceMultiplier': float(self.price_multiplier) if self.price_multiplier else 0,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }

    def __repr__(self):
        return f'<TicketClass {self.id}: {self.class_name}>'
