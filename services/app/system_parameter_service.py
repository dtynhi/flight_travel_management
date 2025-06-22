from repositories.system_parameter_repository import SystemParameterRepository
from models.system_parameter_model import SystemParameter

class SystemParameterService:
    @staticmethod
    def get_all_parameters():
        """Get all system parameters"""
        parameters = SystemParameterRepository.find_all()
        return [param.to_dict() for param in parameters]
    
    @staticmethod
    def get_parameter_by_id(param_id: int):
        """Get system parameter by ID"""
        parameter = SystemParameterRepository.find_by_id(param_id)
        if not parameter:
            raise ValueError(f"System parameter with ID {param_id} not found")
        return parameter.to_dict()
    
    @staticmethod
    def get_current_parameters():
        """Get current active system parameters"""
        parameter = SystemParameterRepository.get_current_parameters()
        if not parameter:
            # Return default values if no parameters exist
            return {
                'number_of_airports': 10,
                'minimum_flight_duration': 30,
                'max_intermediate_stops': 2,
                'minimum_stop_duration': 10,
                'maximum_stop_duration': 20,
                'booking_deadline': 4  # hours before departure
            }
        return parameter.to_dict()
    
    @staticmethod
    def create_parameter(data: dict):
        """Create new system parameter"""
        # Validate data
        SystemParameterService._validate_parameter_data(data)
        
        parameter = SystemParameter(
            number_of_airports=data.get('number_of_airports'),
            minimum_flight_duration=data.get('minimum_flight_duration'),
            max_intermediate_stops=data.get('max_intermediate_stops'),
            minimum_stop_duration=data.get('minimum_stop_duration'),
            maximum_stop_duration=data.get('maximum_stop_duration'),
            booking_deadline=data.get('booking_deadline')
        )
        
        saved_parameter = SystemParameterRepository.save_parameter(parameter)
        return saved_parameter.to_dict()
    
    @staticmethod
    def update_parameter(param_id: int, data: dict):
        """Update system parameter"""
        parameter = SystemParameterRepository.find_by_id(param_id)
        if not parameter:
            raise ValueError(f"System parameter with ID {param_id} not found")
        
        # Validate data
        SystemParameterService._validate_parameter_data(data)
        
        # Update fields
        if 'number_of_airports' in data:
            parameter.number_of_airports = data['number_of_airports']
        if 'minimum_flight_duration' in data:
            parameter.minimum_flight_duration = data['minimum_flight_duration']
        if 'max_intermediate_stops' in data:
            parameter.max_intermediate_stops = data['max_intermediate_stops']
        if 'minimum_stop_duration' in data:
            parameter.minimum_stop_duration = data['minimum_stop_duration']
        if 'maximum_stop_duration' in data:
            parameter.maximum_stop_duration = data['maximum_stop_duration']
        if 'booking_deadline' in data:
            parameter.booking_deadline = data['booking_deadline']
        
        updated_parameter = SystemParameterRepository.update_parameter(parameter)
        return updated_parameter.to_dict()
    
    @staticmethod
    def delete_parameter(param_id: int):
        """Delete system parameter"""
        parameter = SystemParameterRepository.find_by_id(param_id)
        if not parameter:
            raise ValueError(f"System parameter with ID {param_id} not found")
        
        SystemParameterRepository.delete_parameter(param_id)
        return {"message": "System parameter deleted successfully"}
    
    @staticmethod
    def get_specific_parameter(param_name: str):
        """Get specific parameter value"""
        valid_params = [
            'number_of_airports', 'minimum_flight_duration', 'max_intermediate_stops',
            'minimum_stop_duration', 'maximum_stop_duration', 'booking_deadline'
        ]
        
        if param_name not in valid_params:
            raise ValueError(f"Invalid parameter name. Valid parameters: {', '.join(valid_params)}")
        
        value = SystemParameterRepository.get_parameter_by_name(param_name)
        return {param_name: value}
    
    @staticmethod
    def _validate_parameter_data(data: dict):
        """Validate system parameter data"""
        if 'minimum_flight_duration' in data and data['minimum_flight_duration'] and data['minimum_flight_duration'] < 30:
            raise ValueError("Minimum flight duration must be at least 30 minutes")
        
        if 'max_intermediate_stops' in data and data['max_intermediate_stops'] and data['max_intermediate_stops'] > 5:
            raise ValueError("Maximum intermediate stops cannot exceed 5")
        
        if 'minimum_stop_duration' in data and data['minimum_stop_duration'] and data['minimum_stop_duration'] < 5:
            raise ValueError("Minimum stop duration must be at least 5 minutes")
        
        if 'maximum_stop_duration' in data and data['maximum_stop_duration'] and data['maximum_stop_duration'] > 30:
            raise ValueError("Maximum stop duration cannot exceed 30 minutes")
        
        if ('minimum_stop_duration' in data and 'maximum_stop_duration' in data and 
            data['minimum_stop_duration'] and data['maximum_stop_duration'] and
            data['minimum_stop_duration'] >= data['maximum_stop_duration']):
            raise ValueError("Minimum stop duration must be less than maximum stop duration")
        
        if 'booking_deadline' in data and data['booking_deadline'] and data['booking_deadline'] < 1:
            raise ValueError("Booking deadline must be at least 1 hour before departure")
        
        if 'number_of_airports' in data and data['number_of_airports'] and data['number_of_airports'] < 2:
            raise ValueError("Number of airports must be at least 2")