from app.extensions import db

class SystemParameter(db.Model):
    __tablename__ = 'tbl_system_parameters'
    
    id = db.Column(db.Integer, primary_key=True)
    number_of_airports = db.Column(db.Integer)
    minimum_flight_duration = db.Column(db.Integer)
    max_intermediate_stops = db.Column(db.Integer)
    minimum_stop_duration = db.Column(db.Integer)
    maximum_stop_duration = db.Column(db.Integer)
    booking_deadline = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'number_of_airports': self.number_of_airports,
            'minimum_flight_duration': self.minimum_flight_duration,
            'max_intermediate_stops': self.max_intermediate_stops,
            'minimum_stop_duration': self.minimum_stop_duration,
            'maximum_stop_duration': self.maximum_stop_duration,
            'booking_deadline': self.booking_deadline
        }

    def __repr__(self):
        return f'<SystemParameter {self.id}>'