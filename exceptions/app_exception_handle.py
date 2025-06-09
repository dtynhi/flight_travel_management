import traceback

from flask import jsonify
from marshmallow import ValidationError

from exceptions.app_exception import EntityNotFoundException, BadRequestException
from payload.api_response import ErrorApiResponse
from utils.logging import _logger


def register_error_handlers(app):
    @app.errorhandler(EntityNotFoundException)
    def handle_entity_not_found_exception(error):
        _logger.error("EntityNotFoundException occurred: %s\n%s",
                      str(error), traceback.format_exc())
        return jsonify(ErrorApiResponse(message=str(error)).to_dict()), 404
    
    @app.errorhandler(BadRequestException)
    def handle_bad_request_exception(error: Exception):
        _logger.error("BadRequestException occurred: %s\n%s",
                      str(error), traceback.format_exc())
        return jsonify(ErrorApiResponse(message=str(error)).to_dict()), 400

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        _logger.error("ValidationError occurred: %s\n%s",
                      str(error), traceback.format_exc())
        first_message = list(error.messages.values())[0][0]
        return jsonify(
            ErrorApiResponse(
                message=first_message,
                error=error.messages
            ).to_dict()
        ), 400

    @app.errorhandler(Exception)
    def handle_exception(error):
        _logger.error("An unexpected exception occurred: %s\n%s",
                      str(error), traceback.format_exc())
        return jsonify(ErrorApiResponse(message=str(error)).to_dict()), 500
