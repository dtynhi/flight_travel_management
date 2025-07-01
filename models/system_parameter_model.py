from app.extensions import db

class SystemParameter(db.Model):
    __tablename__ = 'tbl_system_parameters'

    id = db.Column(db.Integer, primary_key=True)

    # QĐ1
    minimum_flight_duration = db.Column(db.Integer, nullable=False)  # phút
    max_intermediate_stops = db.Column(db.Integer, nullable=False)
    minimum_stop_duration = db.Column(db.Integer, nullable=False)    # phút
    maximum_stop_duration = db.Column(db.Integer, nullable=False)    # phút

    # QĐ2

    # QĐ3
    booking_deadline = db.Column(db.Integer, nullable=False)         # giờ trước khi khởi hành

    def to_dict(self):
        return {
            "id": self.id,
            "minimum_flight_duration": self.minimum_flight_duration,
            "max_intermediate_stops": self.max_intermediate_stops,
            "minimum_stop_duration": self.minimum_stop_duration,
            "maximum_stop_duration": self.maximum_stop_duration,
            "booking_deadline": self.booking_deadline
        }

