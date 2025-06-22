from werkzeug.security import generate_password_hash

from app.extensions import db
from constant.constant import Role, Permission, Status
from exceptions.app_exception import BadRequestException, EntityNotFoundException
from models.user_model import User
from repositories.user_repository import UserRepository

class AdminService:
    @staticmethod
    def create_user(email, password, full_name=None, phone_number=None, identification_number=None,
                    role=Role.EMPLOYEE, permissions=[Permission.ALL]):
        """
        Create a new user with specified role and permissions
        Only admins can use this method
        """
        # Check if email already exists
        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            raise BadRequestException("Email already exists")
        
        # Create password hash
        hashed_password = generate_password_hash(password)
        
        # Create user with specified roles and permissions
        new_user = User(
            email=email,
            password=hashed_password,
            full_name=full_name,
            role=role,
            permissions=permissions,
            phone_number=phone_number,
            identification_number=identification_number,
            status=Status.ACTIVE
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Return user data
        return new_user.to_dict()
    
    @staticmethod
    def list_users(role=None, status=None):
        """List all users, optionally filtered by role or status"""
        query = User.query
        
        if role:
            # Filter by role using JSON query
            query = query.filter(User.role.contains([role]))
        
        if status:
            query = query.filter_by(status=status)
        
        users = query.all()
        return [user.to_dict() for user in users]
    
    @staticmethod
    def get_user(user_id):
        """Get a user by ID"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} not found")
        return user.to_dict()
    
    @staticmethod
    def update_user(user_id, data):
        """Update user information"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} not found")
        
        # Update fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        
        if 'identification_number' in data:
            user.identification_number = data['identification_number']
        
        if 'role' in data:
            user.role = data['role']
        
        if 'permissions' in data:
            user.permissions = data['permissions']
        
        # Save changes
        db.session.commit()
        return user.to_dict()
    
    @staticmethod
    def update_user_status(user_id, status):
        """Activate or deactivate a user"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} not found")
        
        if status not in [Status.ACTIVE, Status.INACTIVE]:
            raise BadRequestException("Invalid status value")
        
        user.status = status
        db.session.commit()
        return user.to_dict()
    
    @staticmethod
    def get_employee():
        """Get all employees"""
        employees = UserRepository.get_employees()
        if not employees:
            raise EntityNotFoundException("No employees found")
        
        return [employee.to_dict() for employee in employees]
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user by ID"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} not found")
        
        # Set status to DELETED instead of removing from database
        user.status = Status.DELETED
        db.session.commit()
        
        return {"message": "User deleted successfully", "user_id": user_id}
    
    @staticmethod
    def update_employee(user_id, data):
        """Update an employee's information"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"Employee with ID {user_id} not found")
        
        # Update fields
        if 'full_name' in data:
            user.full_name = data['full_name']
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        
        if 'identification_number' in data:
            user.identification_number = data['identification_number']
            
        if 'role' in data:
            user.role = data['role']
        
        if 'status' in data:
            user.status = data['status']
        
        # Save changes
        db.session.commit()
        return user.to_dict()