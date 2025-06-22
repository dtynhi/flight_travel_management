from flask import Blueprint, request, jsonify
from app.extensions import db
from models.system_parameter_model import SystemParameter

regulation_bp = Blueprint('regulation_bp', __name__, url_prefix='/api/v1/system-parameters')

@regulation_bp.route('', methods=['GET'])
def get_regulation():
    param = SystemParameter.query.first()
    if not param:
        return jsonify({"message": "Không tìm thấy thông số hệ thống."}), 404
    return jsonify(param.to_dict())

@regulation_bp.route('', methods=['PUT'])
def update_regulation():
    data = request.get_json()
    param = SystemParameter.query.first()
    if not param:
        param = SystemParameter()
        db.session.add(param)

    try:
        param.number_of_airports = int(data.get("number_of_airports", param.number_of_airports))
        param.minimum_flight_duration = int(data.get("minimum_flight_duration", param.minimum_flight_duration))
        param.max_intermediate_stops = int(data.get("max_intermediate_stops", param.max_intermediate_stops))
        param.minimum_stop_duration = int(data.get("minimum_stop_duration", param.minimum_stop_duration))
        param.maximum_stop_duration = int(data.get("maximum_stop_duration", param.maximum_stop_duration))
        param.booking_deadline = int(data.get("booking_deadline", param.booking_deadline))

        db.session.commit()
        return jsonify(param.to_dict())
    except Exception as e:
        return jsonify({"message": f"Lỗi cập nhật: {str(e)}"}), 400
