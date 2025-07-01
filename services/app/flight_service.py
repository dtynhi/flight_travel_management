from repositories.flight_repository import FlightRepository
from exceptions.app_exception import BadRequestException, EntityNotFoundException


class FlightService:
    @staticmethod
    def get_all_flights():
        """Get all active flights with airport information"""
        flights = FlightRepository.find_all()
        return [flight.to_dict() for flight in flights]

    @staticmethod
    def search_flights(search_params):
        """Search flights based on parameters"""
        departure_airport = search_params.get("departureAirport")
        arrival_airport = search_params.get("arrivalAirport")
        flight_date = search_params.get("flightDate")

        flights = FlightRepository.search_flights(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            flight_date=flight_date,
        )

        return [flight.to_dict() for flight in flights]

    @staticmethod
    def get_flight_by_id(flight_id: int):
        """Get flight by ID"""
        flight = FlightRepository.find_by_id(flight_id)
        if not flight:
            raise EntityNotFoundException(f"Flight with ID {flight_id} not found")
        return flight.to_dict()

    @staticmethod
    def create_flight(data: dict):
        """Create new flight"""
        # Add validation and flight creation logic here
        pass

    @staticmethod
    def update_flight(flight_id: int, data: dict):
        """Update flight"""
        # Add flight update logic here
        pass
