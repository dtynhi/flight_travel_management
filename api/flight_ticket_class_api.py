from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from payload.api_response import SuccessApiResponse, ErrorApiResponse
from services.app.flight_ticket_class_service import FlightTicketClassService
from exceptions.app_exception import EntityNotFoundException, BadRequestException

flight_ticket_class_bp = Blueprint('flight_ticket_class', __name__)

@flight_ticket_class_bp.route('/', methods=['GET'])
def get_all_flight_ticket_classes():
    """Get all flight ticket classes"""
    try:
        flight_ticket_classes = FlightTicketClassService.get_all_flight_ticket_classes()
        return jsonify(SuccessApiResponse(data={
            'flightTicketClasses': flight_ticket_classes,
            'total': len(flight_ticket_classes)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>', methods=['GET'])
def get_ticket_classes_by_flight(flight_id):
    """Get all ticket classes for a specific flight"""
    try:
        ticket_classes = FlightTicketClassService.get_ticket_classes_by_flight(flight_id)
        return jsonify(SuccessApiResponse(data={
            'flightId': flight_id,
            'ticketClasses': ticket_classes,
            'total': len(ticket_classes),
        }).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/ticket-class/<int:ticket_class_id>', methods=['GET'])
def get_flights_by_ticket_class(ticket_class_id):
    """Get all flights for a specific ticket class"""
    try:
        flights = FlightTicketClassService.get_flights_by_ticket_class(ticket_class_id)
        return jsonify(SuccessApiResponse(data={
            'ticketClassId': ticket_class_id,
            'flights': flights,
            'total': len(flights)
        }).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>/ticket-class/<int:ticket_class_id>', methods=['GET'])
def get_flight_ticket_class(flight_id, ticket_class_id):
    """Get specific flight ticket class"""
    try:
        flight_ticket_class = FlightTicketClassService.get_flight_ticket_class(flight_id, ticket_class_id)
        return jsonify(SuccessApiResponse(data=flight_ticket_class).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>/available', methods=['GET'])
def get_available_classes_for_flight(flight_id):
    """Get available ticket classes for a flight"""
    try:
        available_classes = FlightTicketClassService.get_available_classes_for_flight(flight_id)
        return jsonify(SuccessApiResponse(data={
            'flightId': flight_id,
            'availableClasses': available_classes,
            'total': len(available_classes)
        }).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/', methods=['POST'])
@jwt_required()
def create_flight_ticket_class():
    """Create new flight ticket class (Admin only)"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequestException("Request body is required")
        
        flight_ticket_class = FlightTicketClassService.create_flight_ticket_class(data)
        return jsonify(SuccessApiResponse(
            data=flight_ticket_class, 
            message="Flight ticket class created successfully"
        ).to_dict()), 201
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>/ticket-class/<int:ticket_class_id>', methods=['PUT'])
@jwt_required()
def update_flight_ticket_class(flight_id, ticket_class_id):
    """Update flight ticket class (Admin only)"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequestException("Request body is required")
        
        flight_ticket_class = FlightTicketClassService.update_flight_ticket_class(
            flight_id, ticket_class_id, data
        )
        return jsonify(SuccessApiResponse(
            data=flight_ticket_class, 
            message="Flight ticket class updated successfully"
        ).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>/ticket-class/<int:ticket_class_id>', methods=['DELETE'])
@jwt_required()
def delete_flight_ticket_class(flight_id, ticket_class_id):
    """Delete flight ticket class (Admin only)"""
    try:
        result = FlightTicketClassService.delete_flight_ticket_class(flight_id, ticket_class_id)
        return jsonify(SuccessApiResponse(
            data=result, 
            message="Flight ticket class deleted successfully"
        ).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_ticket_class_bp.route('/flight/<int:flight_id>/ticket-class/<int:ticket_class_id>/seats', methods=['PATCH'])
@jwt_required()
def update_seat_availability(flight_id, ticket_class_id):
    """Update seat availability (for booking/cancellation)"""
    try:
        data = request.get_json()
        if not data or 'seatsChange' not in data:
            raise BadRequestException("seatsChange is required")
        
        flight_ticket_class = FlightTicketClassService.update_seat_availability(
            flight_id, ticket_class_id, data['seatsChange']
        )
        return jsonify(SuccessApiResponse(
            data=flight_ticket_class, 
            message="Seat availability updated successfully"
        ).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500