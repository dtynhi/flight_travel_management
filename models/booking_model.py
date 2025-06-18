from app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ticket_class = db.Column(db.String(50), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
