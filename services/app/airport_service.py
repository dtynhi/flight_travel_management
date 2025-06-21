from repositories.airport_repository import AirportRepository
from exceptions.app_exception import BadRequestException, EntityNotFoundException
from models.airport_model import Airport
from app.extensions import db

class AirportService:
    @staticmethod
    def get_all_airports():
        """Get all active airports"""
        airports = AirportRepository.find_all()
        return [airport.to_dict() for airport in airports]
    
    @staticmethod
    def get_airport_by_id(airport_id: int):
        """Get airport by ID"""
        airport = AirportRepository.find_by_id(airport_id)
        if not airport:
            raise EntityNotFoundException(f"Airport with ID {airport_id} not found")
        return airport.to_dict()
    
    @staticmethod
    def search_airports(name: str):
        """Search airports by name"""
        if not name or name.strip() == '':
            return AirportService.get_all_airports()
        
        airports = AirportRepository.find_by_name(name)
        return [airport.to_dict() for airport in airports]
    
    @staticmethod
    def create_airport(data: dict):
        """Create new airport"""
        airport_name = data.get('airport_name')
        if not airport_name:
            raise BadRequestException("Airport name is required")
        
        # Check if airport already exists
        existing_airport = AirportRepository.find_by_exact_name(airport_name)
        if existing_airport:
            raise BadRequestException("Airport with this name already exists")
        
        airport = Airport(
            airport_name=airport_name,
            status=data.get('status', 'ACTIVE')
        )
        
        saved_airport = AirportRepository.save_airport(airport)
        return saved_airport.to_dict()
    
    @staticmethod
    def update_airport(airport_id: int, data: dict):
        """Update airport information"""
        airport = AirportRepository.find_by_id(airport_id)
        if not airport:
            raise EntityNotFoundException(f"Airport with ID {airport_id} not found")
        
        # Update fields
        if 'airport_name' in data:
            airport.airport_name = data['airport_name']
        
        if 'status' in data:
            airport.status = data['status']
        
        updated_airport = AirportRepository.update_airport(airport)
        return updated_airport.to_dict()
    
    @staticmethod
    def update_airport_status(airport_id: int, status: str):
        """Update airport status"""
        airport = AirportRepository.find_by_id(airport_id)
        if not airport:
            raise EntityNotFoundException(f"Airport with ID {airport_id} not found")
        
        if status not in ['ACTIVE', 'INACTIVE']:
            raise BadRequestException("Invalid status. Must be ACTIVE or INACTIVE")
        
        airport.status = status
        updated_airport = AirportRepository.update_airport(airport)
        return updated_airport.to_dict()