import json
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
        reg = RegulationService.get_by_key(key)
        if not reg:
            reg = Regulation(key=key)
            db.session.add(reg)

        reg.value = value
        reg.description = description
        db.session.commit()
        return reg

    @staticmethod
    def get_value(key: str, default=None, parse_json=True):
        reg = RegulationService.get_by_key(key)
        if not reg:
            return default
        try:
            return json.loads(reg.value) if parse_json else reg.value
        except Exception:
            return reg.value
