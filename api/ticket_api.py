from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.app.ticket_service import TicketService
from payload.api_response import SuccessApiResponse

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/', methods=['GET'])
def get_all_tickets():
    tickets = TicketService.get_all_tickets()
    return jsonify(SuccessApiResponse(data=tickets).__dict__)

@ticket_bp.route('/', methods=['POST'])
@jwt_required()
def create_ticket():
    try:
        data = request.get_json()
        ticket = TicketService.create_ticket(data)
        return jsonify(ticket), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json()
    updated_ticket = TicketService.update_ticket(ticket_id, data)
    return jsonify(SuccessApiResponse(data=updated_ticket).__dict__)

@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    TicketService.delete_ticket(ticket_id)
    return jsonify(SuccessApiResponse(message="Xóa vé thành công").__dict__)
