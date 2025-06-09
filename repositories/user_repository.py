from app.extensions import db
from models.user_model import User

class UserRepository:
    @staticmethod
    def find_by_id(user_id: int) -> User:
        return db.session.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def find_by_email(email: str) -> User:
        return db.session.query(User).filter(User.email == email).first()
    
    @staticmethod
    def save_user(user: User):
        db.session.add(user)
        return user
    
    
