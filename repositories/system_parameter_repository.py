from app.extensions import db
from models.system_parameter_model import SystemParameter

class SystemParameterRepository:
    @staticmethod
    def find_all():
        """Get all system parameters"""
        return db.session.query(SystemParameter).all()
    
    @staticmethod
    def find_by_id(param_id: int):
        """Get system parameter by ID"""
        return db.session.query(SystemParameter).filter(SystemParameter.id == param_id).first()
    
    @staticmethod
    def get_current_parameters():
        """Get current active system parameters (usually the latest one)"""
        return db.session.query(SystemParameter).order_by(SystemParameter.id.desc()).first()
    
    @staticmethod
    def save_parameter(parameter: SystemParameter):
        """Save new system parameter"""
        db.session.add(parameter)
        db.session.commit()
        return parameter
    
    @staticmethod
    def update_parameter(parameter: SystemParameter):
        """Update existing system parameter"""
        db.session.commit()
        return parameter
    
    @staticmethod
    def delete_parameter(param_id: int):
        """Delete system parameter"""
        parameter = SystemParameterRepository.find_by_id(param_id)
        if parameter:
            db.session.delete(parameter)
            db.session.commit()
        return parameter
    
    @staticmethod
    def get_parameter_by_name(param_name: str):
        """Get specific parameter value by name"""
        parameter = SystemParameterRepository.get_current_parameters()
        if parameter and hasattr(parameter, param_name):
            return getattr(parameter, param_name)
        return None
    @staticmethod
    def get_current_parameters() -> SystemParameter:
        """Lấy bản ghi cấu hình hệ thống hiện tại (mặc định lấy bản ghi đầu tiên)"""
        return db.session.query(SystemParameter).first()

    @staticmethod
    def update_parameters(params: dict) -> SystemParameter:
        """Cập nhật cấu hình hệ thống"""
        system_param = db.session.query(SystemParameter).first()
        if not system_param:
            system_param = SystemParameter()
            db.session.add(system_param)

        # Gán lại các trường nếu có trong dict
        for key, value in params.items():
            if hasattr(system_param, key):
                setattr(system_param, key, value)

        db.session.commit()
        return system_param

