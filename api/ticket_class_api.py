from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from payload.api_response import SuccessApiResponse, ErrorApiResponse
from services.app.ticket_class_service import TicketClassService
from exceptions.app_exception import EntityNotFoundException, BadRequestException

ticket_class_bp = Blueprint('ticket_class', __name__)

@ticket_class_bp.route('/', methods=['GET'])
def get_all_ticket_classes():
    """Get all ticket classes"""
    try:
        ticket_classes = TicketClassService.get_all_ticket_classes()
        return jsonify(SuccessApiResponse(data={
            'ticketClasses': ticket_classes,
            'total': len(ticket_classes)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@ticket_class_bp.route('/<int:ticket_class_id>', methods=['GET'])
def get_ticket_class(ticket_class_id):
    """Get ticket class by ID"""
    try:
        ticket_class = TicketClassService.get_ticket_class_by_id(ticket_class_id)
        return jsonify(SuccessApiResponse(data=ticket_class).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@ticket_class_bp.route('/search', methods=['GET'])
def search_ticket_classes():
    """Search ticket classes by name"""
    try:
        search_term = request.args.get('name', '')
        ticket_classes = TicketClassService.search_ticket_classes(search_term)
        return jsonify(SuccessApiResponse(data={
            'ticketClasses': ticket_classes,
            'total': len(ticket_classes)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@ticket_class_bp.route('/', methods=['POST'])
@jwt_required()
def create_ticket_class():
    """Create new ticket class (Admin only)"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequestException("Request body is required")
        
        ticket_class = TicketClassService.create_ticket_class(data)
        return jsonify(SuccessApiResponse(data=ticket_class, message="Ticket class created successfully").to_dict()), 201
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@ticket_class_bp.route('/<int:ticket_class_id>', methods=['PUT'])
@jwt_required()
def update_ticket_class(ticket_class_id):
    """Update ticket class (Admin only)"""
    try:
        data = request.get_json()
        if not data:
            raise BadRequestException("Request body is required")
        
        ticket_class = TicketClassService.update_ticket_class(ticket_class_id, data)
        return jsonify(SuccessApiResponse(data=ticket_class, message="Ticket class updated successfully").to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@ticket_class_bp.route('/<int:ticket_class_id>/status', methods=['PATCH'])
@jwt_required()
def update_ticket_class_status(ticket_class_id):
    """Update ticket class status (Admin only)"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            raise BadRequestException("Status is required")
        
        ticket_class = TicketClassService.update_ticket_class_status(ticket_class_id, data['status'])
        return jsonify(SuccessApiResponse(data=ticket_class, message="Ticket class status updated successfully").to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except BadRequestException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500