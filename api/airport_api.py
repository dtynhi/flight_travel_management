from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from payload.api_response import SuccessApiResponse, ErrorApiResponse
from services.app.airport_service import AirportService
from exceptions.app_exception import EntityNotFoundException, BadRequestException

airport_bp = Blueprint('airport', __name__)

@airport_bp.route('/', methods=['GET'])
def get_all_airports():
    """Get all airports"""
    try:
        airports = AirportService.get_all_airports()
        return jsonify(SuccessApiResponse(data=airports).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@airport_bp.route('/<int:airport_id>', methods=['GET'])
def get_airport(airport_id):
    """Get airport by ID"""
    try:
        airport = AirportService.get_airport_by_id(airport_id)
        return jsonify(SuccessApiResponse(data=airport).to_dict()), 200
    except EntityNotFoundException as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@airport_bp.route('/search', methods=['GET'])
def search_airports():
    """Search airports by name"""
    try:
        search_term = request.args.get('name', '')
        airports = AirportService.search_airports(search_term)
        return jsonify(SuccessApiResponse(data=airports).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@airport_bp.route('/', methods=['POST'])
@jwt_required()
def create_airport():
    """Create new airport (Admin only)"""
    AirportService.create_airport(request.json)
    return jsonify(SuccessApiResponse().to_dict()), 201

@airport_bp.route('/<int:airport_id>', methods=['PUT'])
@jwt_required()
def update_airport(airport_id):
    airport = AirportService.update_airport(airport_id, request.json)
    return jsonify(SuccessApiResponse(data=airport).to_dict()), 200

@airport_bp.route('/<int:airport_id>/status', methods=['PATCH'])  # Changed to PATCH
@jwt_required()
def update_airport_status(airport_id):
    """Update airport status (Admin only)"""
    pass

@airport_bp.route('/<int:airport_id>', methods=['DELETE'])
@jwt_required()
def delete_airport(airport_id):
    AirportService.delete_airport(airport_id)
    return jsonify(SuccessApiResponse().to_dict()), 200