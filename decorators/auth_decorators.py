from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from payload.api_response import ErrorApiResponse
from services.app.user_service import UserService
from constant.constant import Permission


def has_authority(roles=[], permissions=[], all_roles_required=False, all_permissions_required=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_identity = get_jwt_identity()
            if not user_identity:
                return jsonify(ErrorApiResponse(message="Unauthorized: User ID missing in token").to_dict()), 401

            user = UserService.get_user_by_id(int(user_identity))
            if not user:
                return jsonify(ErrorApiResponse(message="User not found").to_dict()), 404

            user_roles = user.get("roles", [])
            user_permissions = user.get("permissions", [])

            if all_roles_required:
                if not all(role in user_roles for role in roles):
                    return jsonify(ErrorApiResponse(message="Unauthorized: Insufficient roles").to_dict()), 403
            else:
                if not any(role in user_roles for role in roles):
                    return jsonify(ErrorApiResponse(message="Unauthorized: Insufficient roles").to_dict()), 403

            if not permissions:
                return fn(*args, **kwargs)
            else :
                if all_permissions_required:
                    if not all(permission in user_permissions for permission in permissions):
                        return jsonify(ErrorApiResponse(message="Unauthorized: Insufficient permissions").to_dict()), 403
                else:
                    if not any(permission in user_permissions for permission in permissions):
                        return jsonify(ErrorApiResponse(message="Unauthorized: Insufficient permissions").to_dict()), 403
                    return fn(*args, **kwargs)

        return decorator

    return wrapper
