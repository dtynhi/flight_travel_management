from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from payload.api_response import SuccessApiResponse, ErrorApiResponse
from services.app.flight_service import FlightService

flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/search', methods=['GET'])
def search_flights():
    """Search flights with optional filters"""
    try:
        search_params = {
            'departureAirport': request.args.get('departureAirport'),
            'arrivalAirport': request.args.get('arrivalAirport'),
            'flightDate': request.args.get('flightDate')
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v}
        
        flights = FlightService.search_flights(search_params)
        
        return jsonify(SuccessApiResponse(data={
            'flights': flights,
            'total': len(flights)
        }).to_dict()), 200
        
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/', methods=['GET'])
def get_all_flights():
    """Get all flights"""
    try:
        flights = FlightService.get_all_flights()
        return jsonify(SuccessApiResponse(data={
            'flights': flights,
            'total': len(flights)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    """Get flight by ID"""
    flight = FlightService.get_flight_by_id(flight_id)
    return jsonify(SuccessApiResponse(data=flight).to_dict()), 200

# PROTECTED - Authentication required
@flight_bp.route('/', methods=['POST'])
@jwt_required()
def create_flight():
    """Create flight - ADMIN ONLY"""
    # Check if user is admin
    current_user = get_jwt_identity()
    # Add admin check logic
    pass