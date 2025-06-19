from app.extensions import db
from models.airport_model import Airport
from sqlalchemy import and_, or_, func

class AirportRepository:
    @staticmethod
    def find_all():
        """Get all active airports (case-insensitive)"""
        return db.session.query(Airport).filter(
            or_(
                Airport.status.ilike('active'),   # Matches 'active', 'ACTIVE', 'Active'
                Airport.status.ilike('ACTIVE'),
                Airport.status.is_(None)
            )
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def find_by_id(airport_id: int):
        """Get airport by ID"""
        return db.session.query(Airport).filter(Airport.id == airport_id).first()
    
    @staticmethod
    def find_by_name(name: str):
        """Find airports by name (partial match)"""
        return db.session.query(Airport).filter(
            and_(
                Airport.airport_name.ilike(f'%{name}%'),
                or_(
                    Airport.status.ilike('active'),
                    Airport.status.ilike('ACTIVE'),
                    Airport.status.is_(None)
                )
            )
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def find_by_exact_name(name: str):
        """Find airport by exact name"""
        return db.session.query(Airport).filter(
            and_(
                Airport.airport_name == name,
                or_(
                    Airport.status.ilike('active'),
                    Airport.status.ilike('ACTIVE'),
                    Airport.status.is_(None)
                )
            )
        ).first()
    
    @staticmethod
    def save_airport(airport: Airport):
        """Save new airport"""
        db.session.add(airport)
        db.session.commit()
        return airport
    
    @staticmethod
    def update_airport(airport: Airport):
        """Update existing airport"""
        db.session.commit()
        return airport
    
    @staticmethod
    def delete_airport(airport_id: int):
        """Soft delete airport by setting status to INACTIVE"""
        airport = AirportRepository.find_by_id(airport_id)
        if airport:
            airport.status = 'INACTIVE'
            db.session.commit()
        return airport
    
    @staticmethod
    def find_active_airports():
        """Get only airports with ACTIVE/active status"""
        return db.session.query(Airport).filter(
            or_(
                Airport.status.ilike('active'),
                Airport.status.ilike('ACTIVE')
            )
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def find_inactive_airports():
        """Get only airports with INACTIVE status"""
        return db.session.query(Airport).filter(
            Airport.status.ilike('INACTIVE')
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def count_all():
        """Count total airports"""
        return db.session.query(Airport).count()
    
    @staticmethod
    def count_active():
        """Count active airports (case-insensitive)"""
        return db.session.query(Airport).filter(
            or_(
                Airport.status.ilike('active'),
                Airport.status.ilike('ACTIVE'),
                Airport.status.is_(None)
            )
        ).count()
    
    @staticmethod
    def search_by_keyword(keyword: str):
        """Search airports by keyword in name"""
        if not keyword or keyword.strip() == '':
            return AirportRepository.find_all()
        
        return db.session.query(Airport).filter(
            and_(
                Airport.airport_name.ilike(f'%{keyword}%'),
                or_(
                    Airport.status.ilike('active'),
                    Airport.status.ilike('ACTIVE'),
                    Airport.status.is_(None)
                )
            )
        ).order_by(Airport.airport_name).all()
    
    @staticmethod
    def is_active_status(status: str):
        """Helper method to check if status is considered active"""
        if not status:
            return True  # None/empty is considered active
        return status.lower() in ['active', 'ACTIVE']
    
    @staticmethod
    def normalize_status(status: str):
        """Helper method to normalize status to uppercase"""
        if not status:
            return 'ACTIVE'
        return status.upper()