from flask import Blueprint, request, jsonify
from models.flight_model import Flight
from models.ticket_class_model import TicketClass
from models.intermediate_airport_model import IntermediateAirport
from models.airport_model import Airport
from models.flight_ticket_class_model import FlightTicketClass
from models.system_parameter_model import SystemParameter
from payload.api_response import SuccessApiResponse, ErrorApiResponse
from datetime import datetime, timedelta, timezone
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.app.flight_service import FlightService

flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/search', methods=['GET'])
def search_flights():
    try:
        search_params = {
            'departureAirport': request.args.get('departureAirport'),
            'arrivalAirport': request.args.get('arrivalAirport'),
            'flightDate': request.args.get('flightDate')
        }
        search_params = {k: v for k, v in search_params.items() if v}
        flights = FlightService.search_flights(search_params)
        return jsonify(SuccessApiResponse(data={
            'flights': flights,
            'total': len(flights)
        }).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message='Lỗi khi tìm kiếm chuyến bay: ' + str(e)).to_dict()), 500

@flight_bp.route('/airports', methods=['GET'])
def get_airports():
    try:
        airports = Airport.query.all()
        data = [{'id': a.id, 'airport_name': a.airport_name} for a in airports]
        return jsonify(SuccessApiResponse(data=data).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message='Không lấy được danh sách sân bay: ' + str(e)).to_dict()), 500

@flight_bp.route('/', methods=['POST'])
@jwt_required()
def create_flight():
    try:
        data = request.json
        from_airport = data.get("from_airport")
        to_airport = data.get("to_airport")
        departure_time = data.get("departure_time")
        flight_time_minutes = int(data.get("flight_time_minutes"))
        base_price = float(data.get("base_price"))
        stops = data.get("intermediate_airports", [])
        seat_config = data.get("seat_config", [])

        # Lấy tham số hệ thống
        sys_param = SystemParameter.query.first()
        if not sys_param:
            return jsonify(ErrorApiResponse(message="Không tìm thấy cấu hình hệ thống").to_dict()), 400

        if from_airport == to_airport:
            return jsonify(ErrorApiResponse(message="Sân bay đi và đến không được giống nhau").to_dict()), 400

        if flight_time_minutes < sys_param.minimum_flight_duration:
            return jsonify(ErrorApiResponse(message=f"Thời gian bay tối thiểu là {sys_param.minimum_flight_duration} phút").to_dict()), 400

        if len(stops) > sys_param.max_intermediate_stops:
            return jsonify(ErrorApiResponse(message=f"Chỉ được tối đa {sys_param.max_intermediate_stops} sân bay trung gian").to_dict()), 400

        for stop in stops:
            if stop['id'] in [from_airport, to_airport]:
                return jsonify(ErrorApiResponse(message="Sân bay trung gian không được trùng sân bay đi/đến").to_dict()), 400
            if not (sys_param.minimum_stop_duration <= stop['stop_duration'] <= sys_param.maximum_stop_duration):
                return jsonify(ErrorApiResponse(
                    message=f"Thời gian dừng phải từ {sys_param.minimum_stop_duration} đến {sys_param.maximum_stop_duration} phút"
                ).to_dict()), 400

        departure_dt = datetime.fromisoformat(departure_time)
        total_stop = sum([int(s['stop_duration']) for s in stops])
        arrival_time = departure_dt + timedelta(minutes=flight_time_minutes + total_stop)

        flight = Flight(
            departure_airport_id=from_airport,
            arrival_airport_id=to_airport,
            departure_time=departure_dt,
            arrival_time=arrival_time,
            base_price=base_price,
            flight_duration=flight_time_minutes,
            status='ACTIVE'
        )
        db.session.add(flight)
        db.session.commit()

        for stop in stops:
            db.session.add(IntermediateAirport(
                flight_id=flight.id,
                intermediate_airport_id=stop['id'],
                stop_order=stop['stop_order'],
                stop_duration=stop['stop_duration'],
                notes=stop.get('note', ''),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ))

        for item in seat_config:
            db.session.add(FlightTicketClass(
                flight_id=flight.id,
                ticket_class_id=item['ticket_class_id'],
                total_seats=item['total_seats'],
                available_seats=item.get('available_seats', item['total_seats']),
                ticket_price=item['ticket_price'],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ))

        db.session.commit()
        return jsonify(SuccessApiResponse(data={"flight_id": flight.id}).to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message='Lỗi tạo chuyến bay: ' + str(e)).to_dict()), 500

