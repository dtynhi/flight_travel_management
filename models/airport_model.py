from app.extensions import db
from datetime import datetime

class Airport(db.Model):
    __tablename__ = 'tbl_airports'
    
    id = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # ✅ Fixed datetime
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Fixed datetime
    status = db.Column(db.String(20))

    def to_dict(self):
        """Convert airport to dictionary for API response"""
        return {
            'id': self.id,
            'airportName': self.airport_name,
            'name': self.airport_name, 
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }

    def __repr__(self):
        return f'<Airport {self.id}: {self.airport_name}>'