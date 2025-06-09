from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.extensions import db
from exceptions.app_exception import BadRequestException
from models.user_model import User
from repositories.user_repository import UserRepository
from constant.constant import Role

class AuthService:
    @staticmethod
    def register(email, password, full_name=None, phone_number=None, identification_number=None):
        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            raise BadRequestException("Email already exists")
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password,
            full_name=full_name,
            roles=Role.USER,
            phone_number=phone_number,
            identification_number=identification_number,
            status="ACTIVE"
        )
        
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    
    @staticmethod
    def login(username: str, password: str):
        if not username or not password:
            raise BadRequestException("Username or password is missing")
        user = UserRepository.find_by_email(username)
        if not user:
            raise BadRequestException("User not found")
        if not check_password_hash(user.password, password):
            raise BadRequestException("Incorrect password")
        return user.to_dict()

    @staticmethod
    def change_pwd(user_id: int, old_pwd: str, new_pwd: str):
        if not user_id or not old_pwd or not new_pwd:
            raise BadRequestException("User ID, old password or new password is missing")
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise BadRequestException("User not found")
        if not check_password_hash(user.password, old_pwd):
            raise BadRequestException("Incorrect old password")
        user.password = generate_password_hash(new_pwd)
        db.session().commit()
        return user.to_dict()

    @staticmethod
    def create_token(user: User):
        if not user:
            raise BadRequestException("User is missing")
        return create_access_token(identity=str(user['id']))
