from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.app.system_parameter_service import SystemParameterService
from payload.api_response import SuccessApiResponse, ErrorApiResponse

system_parameter_bp = Blueprint('system_parameter', __name__)

@system_parameter_bp.route('/', methods=['GET'])
def get_all_parameters():
    """Get all system parameters"""
    try:
        parameters = SystemParameterService.get_all_parameters()
        return jsonify(SuccessApiResponse(data={
            'parameters': parameters,
            'total': len(parameters)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/current', methods=['GET'])
def get_current_parameters():
    """Get current active system parameters"""
    try:
        parameters = SystemParameterService.get_current_parameters()
        return jsonify(SuccessApiResponse(data=parameters).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/<int:param_id>', methods=['GET'])
def get_parameter(param_id):
    """Get system parameter by ID"""
    try:
        parameter = SystemParameterService.get_parameter_by_id(param_id)
        return jsonify(SuccessApiResponse(data=parameter).to_dict()), 200
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/', methods=['POST'])
@jwt_required()
def create_parameter():
    """Create new system parameter - ADMIN ONLY"""
    try:
        data = request.json
        if not data:
            return jsonify(ErrorApiResponse(message="Request data is required").to_dict()), 400
        
        parameter = SystemParameterService.create_parameter(data)
        return jsonify(SuccessApiResponse(data=parameter).to_dict()), 201
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/<int:param_id>', methods=['PUT'])
@jwt_required()
def update_parameter(param_id):
    """Update system parameter - ADMIN ONLY"""
    try:
        data = request.json
        if not data:
            return jsonify(ErrorApiResponse(message="Request data is required").to_dict()), 400
        
        parameter = SystemParameterService.update_parameter(param_id, data)
        return jsonify(SuccessApiResponse(data=parameter).to_dict()), 200
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/<int:param_id>', methods=['PATCH'])
@jwt_required()
def update_parameter_partial(param_id):
    """Partially update system parameter - ADMIN ONLY"""
    try:
        data = request.json
        if not data:
            return jsonify(ErrorApiResponse(message="Request data is required").to_dict()), 400
        
        parameter = SystemParameterService.update_parameter(param_id, data)
        return jsonify(SuccessApiResponse(data=parameter).to_dict()), 200
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/<int:param_id>', methods=['DELETE'])
@jwt_required()
def delete_parameter(param_id):
    """Delete system parameter - ADMIN ONLY"""
    try:
        result = SystemParameterService.delete_parameter(param_id)
        return jsonify(SuccessApiResponse(data=result).to_dict()), 200
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 404
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@system_parameter_bp.route('/param/<string:param_name>', methods=['GET'])
def get_specific_parameter(param_name):
    """Get specific parameter value by name"""
    try:
        parameter = SystemParameterService.get_specific_parameter(param_name)
        return jsonify(SuccessApiResponse(data=parameter).to_dict()), 200
    except ValueError as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 400
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500