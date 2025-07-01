from flask import Blueprint, request, jsonify
from app.extensions import db
from models.system_parameter_model import SystemParameter

regulation_bp = Blueprint(
    "regulation_bp", __name__, url_prefix="/api/v1/system-parameters"
)


@regulation_bp.route("", methods=["GET"])
def get_regulation():
    param = SystemParameter.query.order_by(SystemParameter.id.desc()).first()
    if not param:
        return jsonify({"message": "Không tìm thấy thông số hệ thống."}), 404
    return jsonify(param.to_dict())


@regulation_bp.route("", methods=["PUT"])
@regulation_bp.route("/", methods=["PUT"])
def update_regulation():
    data = request.get_json()
    # Lấy bản ghi mới nhất
    param = SystemParameter.query.order_by(SystemParameter.id.desc()).first()

    try:
        if not param:
            # Nếu chưa có thì tạo mới
            param = SystemParameter(
                minimum_flight_duration=int(data.get("minimum_flight_duration", 0)),
                max_intermediate_stops=int(data.get("max_intermediate_stops", 0)),
                minimum_stop_duration=int(data.get("minimum_stop_duration", 0)),
                maximum_stop_duration=int(data.get("maximum_stop_duration", 0)),
                booking_deadline=int(data.get("booking_deadline", 0)),
            )
            db.session.add(param)
        else:
            # Nếu đã có thì cập nhật
            param.minimum_flight_duration = int(
                data.get("minimum_flight_duration", param.minimum_flight_duration)
            )
            param.max_intermediate_stops = int(
                data.get("max_intermediate_stops", param.max_intermediate_stops)
            )
            param.minimum_stop_duration = int(
                data.get("minimum_stop_duration", param.minimum_stop_duration)
            )
            param.maximum_stop_duration = int(
                data.get("maximum_stop_duration", param.maximum_stop_duration)
            )
            param.booking_deadline = int(
                data.get("booking_deadline", param.booking_deadline)
            )

        db.session.commit()
        return jsonify(param.to_dict())
    except Exception as e:
        return jsonify({"message": f"Lỗi cập nhật: {str(e)}"}), 400
