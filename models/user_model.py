from app.extensions import db
from constant.constant import Role, Permission, Status


class User(db.Model):
    __tablename__ = 'tbl_system_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False) 
    full_name = db.Column(db.String(150), nullable=True)
    identification_number = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True) 
    status = db.Column(db.String(20), nullable=True, default=Status.ACTIVE)  
    role = db.Column(db.String(20), nullable=False, default=Role.USER)
    permissions = db.Column(db.JSON, nullable=False, default=[Permission.ALL])

    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'identification_number': self.identification_number,
            'phone_number': self.phone_number,
            'status': self.status,
            'role': self.role,
            'permissions': self.permissions
        }