import os
import sys
from datetime import timedelta

from dotenv import load_dotenv


class AppConfig:
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = None
    JWT_SECRET_KEY = None
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(14400))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(86400))
    JWT_TOKEN_LOCATION = 'cookies'
    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEBUG = False
    LOG_FILE_PATH = None
    SESSION_COOKIE_NAME = "access_token_cookie"
    CORS_ORIGINS = []
    COOKIE_DOMAIN = None
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False
    ROOT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    SCHEDULER_API_ENABLED = True
    X_API_KEY = None
    ROOT_FOLDER = None
    ROOT_ORGANIZATION_ID = None

    @staticmethod
    def load():
        os.environ.setdefault('FLASK_ENV', 'development')
        
        is_dev_mode = os.environ.get('FLASK_ENV') == 'development'
        AppConfig.ROOT_DIR = is_dev_mode and os.path.abspath(os.path.dirname(__file__)) or os.path.abspath(os.path.dirname(sys.argv[0]))
        dotenv_path = is_dev_mode and os.path.join(AppConfig.ROOT_DIR, '..', '.env.dev') or os.path.join(AppConfig.ROOT_DIR, '.env.prod')
        
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            print(f"Loaded environment variables from {dotenv_path}")
        else:
            print(f"Environment file not found: {dotenv_path}")

        AppConfig.FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
        AppConfig.FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
        AppConfig.SQLALCHEMY_TRACK_MODIFICATIONS = AppConfig.FLASK_ENV == 'development'
        
        AppConfig.SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
            
        AppConfig.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        AppConfig.JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 14400)))
        AppConfig.JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 86400)))
        AppConfig.JWT_TOKEN_LOCATION = 'cookies'

        AppConfig.MAIL_SERVER = os.environ.get('MAIL_SERVER')
        AppConfig.MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
        AppConfig.MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
        AppConfig.MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        AppConfig.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        AppConfig.MAIL_DEBUG = os.environ.get('MAIL_DEBUG', 'false').lower() == 'true'
        
        AppConfig.LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 'logs/')
        os.makedirs(AppConfig.LOG_FILE_PATH, exist_ok=True) 
        
        AppConfig.SESSION_COOKIE_NAME = "access_token_cookie"
        AppConfig.CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
        AppConfig.COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN')
        AppConfig.JWT_COOKIE_CSRF_PROTECT = False
        AppConfig.JWT_COOKIE_SECURE = AppConfig.FLASK_ENV == 'production'

        AppConfig.CACHE_TYPE = 'simple'
        AppConfig.CACHE_DEFAULT_TIMEOUT = 300
        AppConfig.SCHEDULER_API_ENABLED = True