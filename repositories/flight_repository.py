from app.extensions import db
from models.flight_model import Flight
from models.airport_model import Airport
from sqlalchemy import and_, or_, func
from datetime import datetime

class FlightRepository:
    @staticmethod
    def find_all():
        """Get all active flights with airport relationships"""
        return db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(
            or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
        ).order_by(Flight.departure_time.asc()).all()
    
    @staticmethod
    def find_by_id(flight_id: int):
        """Get flight by ID with airport relationships"""
        return db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(Flight.id == flight_id).first()
    
    @staticmethod
    def search_flights(departure_airport=None, arrival_airport=None, flight_date=None):
        """Search flights with filters"""
        query = db.session.query(Flight).options(
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        )
        
        # Filter by departure airport name
        if departure_airport:
            query = query.join(
                Airport, Flight.departure_airport_id == Airport.id
            ).filter(
                Airport.airport_name.ilike(f'%{departure_airport}%')
            )
        
        # Filter by arrival airport name
        if arrival_airport:
            # Create alias for second join to avoid conflicts
            arrival_airport_alias = db.aliased(Airport)
            query = query.join(
                arrival_airport_alias, Flight.arrival_airport_id == arrival_airport_alias.id
            ).filter(
                arrival_airport_alias.airport_name.ilike(f'%{arrival_airport}%')
            )
        
        # Filter by flight date
        if flight_date:
            try:
                date_obj = datetime.strptime(flight_date, '%Y-%m-%d').date()
                query = query.filter(func.date(Flight.departure_time) == date_obj)
            except ValueError:
                # Invalid date format, ignore filter
                pass
        
        # Filter by status
        query = query.filter(
            or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
        )
        
        return query.order_by(Flight.departure_time.asc()).all()
    
    @staticmethod
    def save_flight(flight: Flight):
        """Save new flight"""
        db.session.add(flight)
        db.session.commit()
        return flight
    
    @staticmethod
    def update_flight(flight: Flight):
        """Update existing flight"""
        db.session.commit()
        return flight
    
    @staticmethod
    def delete_flight(flight_id: int):
        """Soft delete flight by setting status to INACTIVE"""
        flight = FlightRepository.find_by_id(flight_id)
        if flight:
            flight.status = 'INACTIVE'
            db.session.commit()
        return flight
    
    @staticmethod
    def find_by_route(departure_airport_id: int, arrival_airport_id: int):
        """Find flights by specific route"""
        return db.session.query(Flight).filter(
            and_(
                Flight.departure_airport_id == departure_airport_id,
                Flight.arrival_airport_id == arrival_airport_id,
                or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
            )
        ).order_by(Flight.departure_time.asc()).all()
    
    @staticmethod
    def find_by_date_range(start_date, end_date):
        """Find flights within date range"""
        return db.session.query(Flight).filter(
            and_(
                Flight.departure_time >= start_date,
                Flight.departure_time <= end_date,
                or_(Flight.status == 'ACTIVE', Flight.status == 'SCHEDULED', Flight.status.is_(None))
            )
        ).order_by(Flight.departure_time.asc()).all()