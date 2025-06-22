from repositories.ticket_class_repository import TicketClassRepository
from models.ticket_class_model import TicketClass
from exceptions.app_exception import BadRequestException, EntityNotFoundException
from datetime import datetime, timezone  # Add timezone import here

class TicketClassService:
    @staticmethod
    def get_all_ticket_classes():
        """Get all active ticket classes"""
        ticket_classes = TicketClassRepository.find_all()
        return [ticket_class.to_dict() for ticket_class in ticket_classes]
    
    @staticmethod
    def search_ticket_classes(search_term):
        """Search ticket classes by name"""
        ticket_classes = TicketClassRepository.search_ticket_classes(search_term=search_term)
        return [ticket_class.to_dict() for ticket_class in ticket_classes]
    
    @staticmethod
    def get_ticket_class_by_id(ticket_class_id: int):
        """Get ticket class by ID"""
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if not ticket_class:
            raise EntityNotFoundException(f"Ticket class with ID {ticket_class_id} not found")
        return ticket_class.to_dict()
    
    @staticmethod
    def create_ticket_class(data: dict):
        """Create new ticket class"""
        # Validate required fields
        if 'className' not in data:
            raise BadRequestException("Class name is required")
        if 'priceMultiplier' not in data:
            raise BadRequestException("Price multiplier is required")
        
        # Check if class name already exists
        existing_class = TicketClassRepository.find_by_name(data['className'])
        if existing_class:
            raise BadRequestException(f"Ticket class '{data['className']}' already exists")
        
        # Validate price multiplier
        try:
            price_multiplier = float(data['priceMultiplier'])
            if price_multiplier <= 0:
                raise BadRequestException("Price multiplier must be greater than 0")
        except ValueError:
            raise BadRequestException("Invalid price multiplier format")
        
        # Create new ticket class
        ticket_class = TicketClass(
            class_name=data['className'],
            price_multiplier=price_multiplier,
            status=data.get('status', 'ACTIVE')
        )
        
        saved_ticket_class = TicketClassRepository.save_ticket_class(ticket_class)
        return saved_ticket_class.to_dict()
    
    @staticmethod
    def update_ticket_class(ticket_class_id: int, data: dict):
        """Update ticket class"""
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if not ticket_class:
            raise EntityNotFoundException(f"Ticket class with ID {ticket_class_id} not found")
        
        # Update fields if provided
        if 'className' in data:
            # Check if new name conflicts with existing class
            existing_class = TicketClassRepository.find_by_name(data['className'])
            if existing_class and existing_class.id != ticket_class_id:
                raise BadRequestException(f"Ticket class '{data['className']}' already exists")
            ticket_class.class_name = data['className']
        
        if 'priceMultiplier' in data:
            try:
                price_multiplier = float(data['priceMultiplier'])
                if price_multiplier <= 0:
                    raise BadRequestException("Price multiplier must be greater than 0")
                ticket_class.price_multiplier = price_multiplier
            except ValueError:
                raise BadRequestException("Invalid price multiplier format")
        
        if 'status' in data:
            ticket_class.status = data['status']
        
        ticket_class.updated_at = datetime.now(timezone.utc)  # Remove extra () here
        updated_ticket_class = TicketClassRepository.update_ticket_class(ticket_class)
        return updated_ticket_class.to_dict()
    
    @staticmethod
    def update_ticket_class_status(ticket_class_id: int, status: str):
        """Update ticket class status"""
        ticket_class = TicketClassRepository.find_by_id(ticket_class_id)
        if not ticket_class:
            raise EntityNotFoundException(f"Ticket class with ID {ticket_class_id} not found")
        
        # Validate status
        valid_statuses = ['ACTIVE', 'INACTIVE']
        if status not in valid_statuses:
            raise BadRequestException(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        ticket_class.status = status
        ticket_class.updated_at = datetime.now(timezone.utc)  # Remove extra () here
        updated_ticket_class = TicketClassRepository.update_ticket_class(ticket_class)
        return updated_ticket_class.to_dict()