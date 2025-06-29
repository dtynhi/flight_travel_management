from flask import Flask
from flask_cors import CORS

from app.extensions import *
from config.app_config import AppConfig
from exceptions.app_exception_handle import register_error_handlers
from utils.logging import set_up_logging


def init_app(app: Flask):
    set_up_logging(app)
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app, resources={
        r"/*": {
            "origins": AppConfig.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "supports_credentials": True
        }
    })
    register_error_handlers(app)
