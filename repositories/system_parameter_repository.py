from app.extensions import db
from models.system_parameter_model import SystemParameter

class SystemParameterRepository:
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

