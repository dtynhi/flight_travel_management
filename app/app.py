from flask import Flask

from api.auth_api import auth_bp
from api.index_api import index_bp
from api.user_api import user_bp
from api.admin_api import admin_bp
from api.flight_api import flight_bp
from api.airport_api import airport_bp
from api.ticket_class_api import ticket_class_bp
from api.flight_ticket_class_api import flight_ticket_class_bp
from app import init_app
from config.app_config import AppConfig

# from services.app.job_service import init_scheduler

AppConfig.load()

app = Flask(__name__, template_folder='/templates', static_url_path='/static')
app.config.from_object(AppConfig)
init_app(app)

# init_scheduler(app)
# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(user_bp, url_prefix='/api/v1/user')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
app.register_blueprint(flight_bp, url_prefix='/api/v1/flight')
app.register_blueprint(airport_bp, url_prefix='/api/v1/airport')
app.register_blueprint(ticket_class_bp, url_prefix='/api/v1/ticket-class')
app.register_blueprint(flight_ticket_class_bp, url_prefix='/api/v1/flight-ticket-class')

app.register_blueprint(index_bp, url_prefix='')
