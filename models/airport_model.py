from app.extensions import db
from datetime import datetime
from constant.constant import Status

class Airport(db.Model):
    __tablename__ = 'tbl_airports'

    id = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=Status.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "airport_name": self.airport_name,
            "status": self.status
        }

