from flask import Blueprint, request, make_response
from payload.api_response import SuccessApiResponse
from services.regulation_service import RegulationService
from validations.regulation_validation import RegulationSchema

regulation_bp = Blueprint("regulation", __name__, url_prefix="/api/v1/regulations")


@regulation_bp.route("", methods=["GET"])
def get_all_regulations():
    regs = RegulationService.get_all()
    data = [
        {"key": r.key, "value": r.value, "description": r.description} for r in regs
    ]
    return make_response(SuccessApiResponse(data=data).to_dict(), 200)


@regulation_bp.route("/<key>", methods=["GET"])
def get_regulation(key):
    reg = RegulationService.get_by_key(key)
    if reg:
        return make_response(
            SuccessApiResponse(
                data={
                    "key": reg.key,
                    "value": reg.value,
                    "description": reg.description,
                }
            ).to_dict(),
            200,
        )
    else:
        return make_response(
            SuccessApiResponse(message="Quy định không tồn tại").to_dict(), 404
        )


@regulation_bp.route("", methods=["PUT"])
def update_or_create_regulation():
    print("🔧 Received PUT /api/v1/regulations")

    data = request.get_json()
    if data is None:
        print("❌ Không nhận được JSON! Có thể thiếu Content-Type hoặc body bị rỗng.")
        return make_response(
            SuccessApiResponse(message="Body rỗng hoặc không phải JSON").to_dict(), 400
        )

    print("📥 Data nhận được:", data)

    try:
        validated_data = RegulationSchema().load(data)
        reg = RegulationService.update_or_create(
            key=validated_data["key"],
            value=validated_data["value"],
            description=validated_data.get("description"),
        )
        return make_response(
            SuccessApiResponse(
                data={
                    "key": reg.key,
                    "value": reg.value,
                    "description": reg.description,
                }
            ).to_dict(),
            200,
        )
    except Exception as e:
        print("❌ Exception khi xử lý quy định:", str(e))
        return make_response(
            SuccessApiResponse(message="Lỗi khi cập nhật quy định").to_dict(), 500
        )
