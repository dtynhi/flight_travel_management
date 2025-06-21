from app.extensions import db
from datetime import datetime, timezone
from constant.constant import Status

class Airport(db.Model):
    __tablename__ = 'tbl_airports'

    id = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=Status.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'airportName': self.airport_name,
            'name': self.airport_name, 
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }
