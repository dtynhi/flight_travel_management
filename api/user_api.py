from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from payload.api_response import SuccessApiResponse
from services.app.auth_service import AuthService
from services.app.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_identity = int(get_jwt_identity())
    user = UserService.get_profile(user_identity)

    response = make_response(SuccessApiResponse(data=user).__dict__)
    return response


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_identity = int(get_jwt_identity())
    payload = request.get_json()
    payload.setdefault('id', user_identity)
    user = UserService.update_profile(payload)
    response = make_response(SuccessApiResponse(data=user).__dict__)
    return response

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def auth_update_pwd():
    data = request.get_json()
    user_identity = int(get_jwt_identity())

    AuthService.change_pwd(user_identity, data['current_password'], data['new_password'])
    return jsonify(SuccessApiResponse(data=None).to_dict()), 200
