from models.regulation_model import Regulation
from app.extensions import db

class RegulationService:
    @staticmethod
    def get_all():
        return Regulation.query.all()

    @staticmethod
    def get_by_key(key):
        return Regulation.query.filter_by(key=key).first()

    @staticmethod
    def update_or_create(key, value, description=None):
        reg = Regulation.query.filter_by(key=key).first()
        if reg:
            reg.value = value
            if description:
                reg.description = description
        else:
            reg = Regulation(key=key, value=value, description=description)
            db.session.add(reg)
        db.session.commit()
        return reg
