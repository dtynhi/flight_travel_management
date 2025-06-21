from app.extensions import db
from models.ticket_class_model import TicketClass
from sqlalchemy import or_

class TicketClassRepository:
    @staticmethod
    def find_all():
        """Get all active ticket classes"""
        return db.session.query(TicketClass).filter(
            or_(TicketClass.status == 'ACTIVE', TicketClass.status.is_(None))
        ).order_by(TicketClass.class_name.asc()).all()
    
    @staticmethod
    def find_by_id(ticket_class_id: int):
        """Get ticket class by ID"""
        return db.session.query(TicketClass).filter(TicketClass.id == ticket_class_id).first()
    
    @staticmethod
    def search_ticket_classes(search_term=None):
        """Search ticket classes by name"""
        query = db.session.query(TicketClass)
        
        # Filter by class name
        if search_term:
            query = query.filter(
                TicketClass.class_name.ilike(f'%{search_term}%')
            )
        
        # Filter by status
        query = query.filter(
            or_(TicketClass.status == 'ACTIVE', TicketClass.status.is_(None))
        )
        
        return query.order_by(TicketClass.class_name.asc()).all()
    
    @staticmethod
    def save_ticket_class(ticket_class: TicketClass):
        """Save new ticket class"""
        db.session.add(ticket_class)
        db.session.commit()
        return ticket_class
    
    @staticmethod
    def update_ticket_class(ticket_class: TicketClass):
        """Update existing ticket class"""
        db.session.commit()
        return ticket_class
    
    @staticmethod
    def delete_ticket_class(ticket_class_id: int):
        """Soft delete ticket class by setting status to INACTIVE"""
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if ticket_class:
            ticket_class.status = 'INACTIVE'
            db.session.commit()
        return ticket_class
    
    @staticmethod
    def find_by_name(class_name: str):
        """Find ticket class by exact name"""
        return db.session.query(TicketClass).filter(
            TicketClass.class_name == class_name
        ).first()