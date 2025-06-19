from app.extensions import db
from models.flight_model import Flight
from models.airport_model import Airport
from sqlalchemy import and_, or_, func
from datetime import datetime

class FlightRepository:
    @staticmethod
    def find_all():
        return db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(
            or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
        ).order_by(Flight.departure_time.asc()).all()
    
    @staticmethod
    def find_by_id(flight_id: int):
        return db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(Flight.id == flight_id).first()
    
    @staticmethod
    def search_flights(departure_airport=None, arrival_airport=None, flight_date=None):
        query = db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        )
        
        if departure_airport:
            query = query.join(Airport, Flight.departure_airport_id == Airport.id).filter(
                Airport.airport_name.ilike(f'%{departure_airport}%')
            )
        
        if arrival_airport:
            arrival_airport_alias = db.aliased(Airport)
            query = query.join(arrival_airport_alias, Flight.arrival_airport_id == arrival_airport_alias.id).filter(
                arrival_airport_alias.airport_name.ilike(f'%{arrival_airport}%')
            )
        
        if flight_date:
            try:
                date_obj = datetime.strptime(flight_date, '%Y-%m-%d').date()
                query = query.filter(func.date(Flight.departure_time) == date_obj)
            except ValueError:
                pass
        
        query = query.filter(
            or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
        )
        
        return query.order_by(Flight.departure_time.asc()).all()

    @staticmethod 
    def save_flight(flight: Flight):
        db.session.add(flight)
        db.session.commit()
        return flight

class AirportRepository:
    @staticmethod
    def find_all():
        return db.session.query(Airport).filter(
            or_(Airport.status == 'ACTIVE', Airport.status.is_(None))
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def find_by_id(airport_id: int):
        return db.session.query(Airport).filter(Airport.id == airport_id).first()
    
    @staticmethod
    def save_airport(airport: Airport):
        db.session.add(airport)
        db.session.commit()
        return airport