import os

from flask import Blueprint, request, send_from_directory

from config.app_config import AppConfig

index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
def index():
    # Return user-agent, IP address, and other request information
    return {
        "user_agent": str(request.user_agent),
        "ip": request.remote_addr,
        "message": "Welcome to the API!"
    }


@index_bp.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(AppConfig.ROOT_DIR, 'static'), "favicon.ico", mimetype='image/vnd.microsoft.icon')


@index_bp.route('/ping', methods=['GET'])
def ping():
    # Return user-agent, IP address, and other request information
    return {
        "message": "Pong!"
    }
