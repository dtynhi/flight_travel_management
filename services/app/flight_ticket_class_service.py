from repositories.flight_ticket_class_repository import FlightTicketClassRepository
from repositories.flight_repository import FlightRepository
from repositories.ticket_class_repository import TicketClassRepository
from models.flight_ticket_class_model import FlightTicketClass
from exceptions.app_exception import BadRequestException, EntityNotFoundException
from datetime import datetime

class FlightTicketClassService:
    @staticmethod
    def get_all_flight_ticket_classes():
        """Get all flight ticket classes"""
        flight_ticket_classes = FlightTicketClassRepository.find_all()
        return [ftc.to_dict() for ftc in flight_ticket_classes]
    
    @staticmethod
    def get_ticket_classes_by_flight(flight_id: int):
        """Get all ticket classes for a specific flight"""
        # Verify flight exists
        flight = FlightRepository.find_by_id(flight_id)
        if not flight:
            raise EntityNotFoundException(f"Flight with ID {flight_id} not found")
        
        flight_ticket_classes = FlightTicketClassRepository.find_by_flight_id(flight_id)
        return [ftc.to_dict() for ftc in flight_ticket_classes]
    
    @staticmethod
    def get_flights_by_ticket_class(ticket_class_id: int):
        """Get all flights for a specific ticket class"""
        # Verify ticket class exists
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if not ticket_class:
            raise EntityNotFoundException(f"Ticket class with ID {ticket_class_id} not found")
        
        flight_ticket_classes = FlightTicketClassRepository.find_by_ticket_class_id(ticket_class_id)
        return [ftc.to_dict() for ftc in flight_ticket_classes]
    
    @staticmethod
    def get_flight_ticket_class(flight_id: int, ticket_class_id: int):
        """Get specific flight ticket class"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if not flight_ticket_class:
            raise EntityNotFoundException(
                f"Flight ticket class not found for flight {flight_id} and class {ticket_class_id}"
            )
        return flight_ticket_class.to_dict()
    
    @staticmethod
    def create_flight_ticket_class(data: dict):
        """Create new flight ticket class"""
        # Validate required fields
        required_fields = ['flightId', 'ticketClassId', 'ticketPrice']
        for field in required_fields:
            if field not in data:
                raise BadRequestException(f"{field} is required")
        
        flight_id = data['flightId']
        ticket_class_id = data['ticketClassId']
        
        # Verify flight and ticket class exist
        flight = FlightRepository.find_by_id(flight_id)
        if not flight:
            raise EntityNotFoundException(f"Flight with ID {flight_id} not found")
        
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if not ticket_class:
            raise EntityNotFoundException(f"Ticket class with ID {ticket_class_id} not found")
        
        # Check if combination already exists
        existing = FlightTicketClassRepository.find_by_flight_and_class(flight_id, ticket_class_id)
        if existing:
            raise BadRequestException(
                f"Flight ticket class already exists for flight {flight_id} and class {ticket_class_id}"
            )
        
        # Validate ticket price
        try:
            ticket_price = float(data['ticketPrice'])
            if ticket_price <= 0:
                raise BadRequestException("Ticket price must be greater than 0")
        except ValueError:
            raise BadRequestException("Invalid ticket price format")
        
        # Validate seats if provided
        total_seats = data.get('totalSeats')
        available_seats = data.get('availableSeats', total_seats)
        
        if total_seats is not None and total_seats < 0:
            raise BadRequestException("Total seats cannot be negative")
        
        if available_seats is not None and available_seats < 0:
            raise BadRequestException("Available seats cannot be negative")
        
        if total_seats is not None and available_seats is not None and available_seats > total_seats:
            raise BadRequestException("Available seats cannot exceed total seats")
        
        # Create new flight ticket class
        flight_ticket_class = FlightTicketClass(
            flight_id=flight_id,
            ticket_class_id=ticket_class_id,
            total_seats=total_seats,
            available_seats=available_seats,
            ticket_price=ticket_price
        )
        
        saved_flight_ticket_class = FlightTicketClassRepository.save_flight_ticket_class(flight_ticket_class)
        return saved_flight_ticket_class.to_dict()
    
    @staticmethod
    def update_flight_ticket_class(flight_id: int, ticket_class_id: int, data: dict):
        """Update flight ticket class"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if not flight_ticket_class:
            raise EntityNotFoundException(
                f"Flight ticket class not found for flight {flight_id} and class {ticket_class_id}"
            )
        
        # Update fields if provided
        if 'ticketPrice' in data:
            try:
                ticket_price = float(data['ticketPrice'])
                if ticket_price <= 0:
                    raise BadRequestException("Ticket price must be greater than 0")
                flight_ticket_class.ticket_price = ticket_price
            except ValueError:
                raise BadRequestException("Invalid ticket price format")
        
        if 'totalSeats' in data:
            total_seats = data['totalSeats']
            if total_seats < 0:
                raise BadRequestException("Total seats cannot be negative")
            flight_ticket_class.total_seats = total_seats
        
        if 'availableSeats' in data:
            available_seats = data['availableSeats']
            if available_seats < 0:
                raise BadRequestException("Available seats cannot be negative")
            if (flight_ticket_class.total_seats is not None and 
                available_seats > flight_ticket_class.total_seats):
                raise BadRequestException("Available seats cannot exceed total seats")
            flight_ticket_class.available_seats = available_seats
        
        flight_ticket_class.updated_at = datetime.utcnow()
        updated_flight_ticket_class = FlightTicketClassRepository.update_flight_ticket_class(flight_ticket_class)
        return updated_flight_ticket_class.to_dict()
    
    @staticmethod
    def delete_flight_ticket_class(flight_id: int, ticket_class_id: int):
        """Delete flight ticket class"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if not flight_ticket_class:
            raise EntityNotFoundException(
                f"Flight ticket class not found for flight {flight_id} and class {ticket_class_id}"
            )
        
        FlightTicketClassRepository.delete_flight_ticket_class(flight_id, ticket_class_id)
        return {"message": "Flight ticket class deleted successfully"}
    
    @staticmethod
    def get_available_classes_for_flight(flight_id: int):
        """Get available ticket classes for a flight"""
        # Verify flight exists
        flight = FlightRepository.find_by_id(flight_id)
        if not flight:
            raise EntityNotFoundException(f"Flight with ID {flight_id} not found")
        
        available_classes = FlightTicketClassRepository.find_available_classes_for_flight(flight_id)
        return [ftc.to_dict() for ftc in available_classes]
    
    @staticmethod
    def update_seat_availability(flight_id: int, ticket_class_id: int, seats_change: int):
        """Update available seats (for booking/cancellation)"""
        flight_ticket_class = FlightTicketClassRepository.find_by_flight_and_class(
            flight_id, ticket_class_id
        )
        if not flight_ticket_class:
            raise EntityNotFoundException(
                f"Flight ticket class not found for flight {flight_id} and class {ticket_class_id}"
            )
        
        new_available_seats = flight_ticket_class.available_seats + seats_change
        
        if new_available_seats < 0:
            raise BadRequestException("Not enough available seats")
        
        if (flight_ticket_class.total_seats is not None and 
            new_available_seats > flight_ticket_class.total_seats):
            raise BadRequestException("Available seats cannot exceed total seats")
        
        updated_flight_ticket_class = FlightTicketClassRepository.update_available_seats(
            flight_id, ticket_class_id, seats_change
        )
        return updated_flight_ticket_class.to_dict()