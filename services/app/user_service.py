from werkzeug.security import generate_password_hash

from app.extensions import db
from constant.constant import Role, Permission
from exceptions.app_exception import BadRequestException
from models.user_model import User
from repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def register_user(user: dict):
        email, password = user['email'], user['password']
        existed_user = UserRepository.find_by_email(email)
        if existed_user:
            raise BadRequestException("Email already exists")
        hash_pwd = generate_password_hash(password)
        new_user = User(email=email, password=hash_pwd, roles=[Role.USER],
                        permissions=[Permission.ALL], is_active=True, is_verified=True)
        UserRepository.save_user(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_profile(user: dict):
        exited_user = UserRepository.find_by_id(user['id'])
        if not exited_user:
            raise BadRequestException("User not found")
        exited_user.full_name = user['full_name']
        exited_user.phone_number = user.get('phone_number', exited_user.phone_number)
        exited_user.identification_number = user.get('identification_number', exited_user.identification_number)
        db.session.commit()
        return exited_user.to_dict()

    @staticmethod
    def get_profile(user_id: int):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise BadRequestException("User not found")
        return user.to_dict()

    @staticmethod
    def get_user_by_id(user_id: int):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return None
        return user.to_dict()
