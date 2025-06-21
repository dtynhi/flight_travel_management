from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required

from constant.constant import Role, Permission
from decorators.auth_decorators import has_authority
from exceptions.app_exception import BadRequestException
from models.user_model import User
from payload.api_response import SuccessApiResponse
from services.app.admin_service import AdminService
from validations.admin_validation import CreateUserSchema

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def create_user():
    """
    Create a new user with specified role
    
    Admin can create users with any role
    """
    try:
        # Validate request data
        data = request.get_json()
        user_data = CreateUserSchema().load(data)
        
        # Create user with specified role
        new_user = AdminService.create_user(
            email=user_data['email'],
            password=user_data['password'],
            full_name=user_data.get('full_name'),
            user_role=user_data.get('user_role', Role.USER),
            phone_number=user_data.get('phone_number'),
            identification_number=user_data.get('identification_number'),
            roles=user_data.get('roles', [Role.EMPLOYEE]),
            permissions=user_data.get('permissions', [Permission.ALL])
        )
        
        # Return success response
        response = make_response(
            SuccessApiResponse(data=new_user).to_dict(),
            201
        )
        return response
        
    except Exception as e:
        # Handle specific exceptions
        if isinstance(e, BadRequestException):
            raise e
        # Log and re-raise other exceptions
        raise BadRequestException(f"Error creating user: {str(e)}")

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def list_users():
    """List all users in the system"""
    
    # Optional filtering parameters
    role_filter = request.args.get('role')
    status_filter = request.args.get('status')
    
    users = AdminService.list_users(role=role_filter, status=status_filter)
    return jsonify(SuccessApiResponse(data=users).to_dict())

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def get_user(user_id):
    """Get details of a specific user"""
    user = AdminService.get_user(user_id)
    return jsonify(SuccessApiResponse(data=user).to_dict())

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def update_user(user_id):
    """Update a user's information and roles"""
    data = request.get_json()
    user = AdminService.update_user(user_id, data)
    return jsonify(SuccessApiResponse(data=user).to_dict())

@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def update_user_status(user_id):
    """Activate or deactivate a user"""
    data = request.get_json()
    status = data.get('status')
    user = AdminService.update_user_status(user_id, status)
    return jsonify(SuccessApiResponse(data=user).to_dict())


@admin_bp.route('/employees', methods=['GET'])
@jwt_required()
@has_authority(roles=[Role.ADMIN])
def list_employees():
    """List all employees in the system"""
    employees = AdminService.list_employees()
    return jsonify(SuccessApiResponse(data=employees).to_dict())