from app.extensions import db
from models.user_model import User

from constant.constant import Role, Status

class UserRepository:
    @staticmethod
    def find_by_id(user_id: int) -> User:
        return db.session.query(User).filter(User.id == user_id and Status.ACTIVE).first()
    
    @staticmethod
    def find_by_email(email: str) -> User:
        return db.session.query(User).filter(User.email == email and User.status == Status.ACTIVE).first()
    
    @staticmethod
    def save_user(user: User):
        db.session.add(user)
        return user

    @staticmethod
    def get_list_employees():
        return db.session.query(User).filter(
            User.role.in_([Role.ADMIN, Role.EMPLOYEE]) & User.status != Status.DELETED
        ).all()
