from app.extensions import db
from models.flight_ticket_class_model import FlightTicketClass
from models.ticket_class_model import TicketClass
from models.flight_model import Flight
from sqlalchemy import and_

class FlightTicketClassRepository:
    @staticmethod
    def find_all():
        """Get all flight ticket classes"""
        return db.session.query(FlightTicketClass).options(
            db.joinedload(FlightTicketClass.ticket_class),
            db.joinedload(FlightTicketClass.flight)
        ).all()
    
    @staticmethod
    def find_by_flight_id(flight_id: int):
        """Get all ticket classes for a specific flight"""
        return db.session.query(FlightTicketClass).options(
            db.joinedload(FlightTicketClass.ticket_class),
            db.joinedload(FlightTicketClass.flight)
        ).filter(FlightTicketClass.flight_id == flight_id).all()
    
    @staticmethod
    def find_by_ticket_class_id(ticket_class_id: int):
        """Get all flights for a specific ticket class"""
        return db.session.query(FlightTicketClass).options(
            db.joinedload(FlightTicketClass.ticket_class),
            db.joinedload(FlightTicketClass.flight)
        ).filter(FlightTicketClass.ticket_class_id == ticket_class_id).all()
    
    @staticmethod
    def find_by_flight_and_class(flight_id: int, ticket_class_id: int):
        """Get specific flight ticket class by composite key"""
        return db.session.query(FlightTicketClass).options(
            db.joinedload(FlightTicketClass.ticket_class),
            db.joinedload(FlightTicketClass.flight)
        ).filter(
            and_(
                FlightTicketClass.flight_id == flight_id,
                FlightTicketClass.ticket_class_id == ticket_class_id
            )
        ).first()
    
    @staticmethod
    def save_flight_ticket_class(flight_ticket_class: FlightTicketClass):
        """Save new flight ticket class"""
        db.session.add(flight_ticket_class)
        db.session.commit()
        return flight_ticket_class
    
    @staticmethod
    def update_flight_ticket_class(flight_ticket_class: FlightTicketClass):
        """Update existing flight ticket class"""
        db.session.commit()
        return flight_ticket_class
    
    @staticmethod
    def delete_flight_ticket_class(flight_id: int, ticket_class_id: int):
        """Delete flight ticket class by composite key"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if flight_ticket_class:
            db.session.delete(flight_ticket_class)
            db.session.commit()
        return flight_ticket_class
    
    @staticmethod
    def update_available_seats(flight_id: int, ticket_class_id: int, seats_change: int):
        """Update available seats for a flight ticket class"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if flight_ticket_class:
            flight_ticket_class.available_seats += seats_change
            db.session.commit()
        return flight_ticket_class
    
    @staticmethod
    def find_available_classes_for_flight(flight_id: int):
        """Get all ticket classes with available seats for a specific flight"""
        return db.session.query(FlightTicketClass).options(
            db.joinedload(FlightTicketClass.ticket_class),
            db.joinedload(FlightTicketClass.flight)
        ).filter(
            and_(
                FlightTicketClass.flight_id == flight_id,
                FlightTicketClass.available_seats > 0
            )
        ).all()