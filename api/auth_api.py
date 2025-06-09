from flask import Blueprint, request, make_response

from payload.api_response import SuccessApiResponse
from services.app.auth_service import AuthService
from services.cookie_service import CookieService
from validations.user_validation import UserSchema, RegisterSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_data = RegisterSchema().load(data)
    
    new_user = AuthService.register(
        email=user_data['email'],
        password=user_data['password'],
        full_name=user_data.get('full_name'),
        phone_number=user_data.get('phone_number'),
        identification_number=user_data.get('identification_number')
    )

    response = make_response(
        SuccessApiResponse(data=new_user).to_dict(),
        201
    )
    CookieService.set_access_token_cookie(
        response,
        AuthService.create_token(new_user)
    )
    return response

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    user_request = UserSchema().load(data)
    user = AuthService.login(user_request['email'], user_request['password'])

    response = make_response(SuccessApiResponse(data=user).to_dict())
    CookieService.set_access_token_cookie(response, AuthService.create_token(user))
    return response

@auth_bp.route('/logout', methods=['GET'])
def auth_logout():
    response = make_response(SuccessApiResponse().to_dict())
    CookieService.delete_access_token_cookie(response)
    return response
