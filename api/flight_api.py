from flask import Blueprint, request, jsonify
from models.flight_model import Flight
from models.ticket_class_model import TicketClass
from models.intermediate_airport_model import IntermediateAirport
from models.airport_model import Airport
from models.flight_ticket_class_model import FlightTicketClass
from payload.api_response import SuccessApiResponse
from datetime import datetime, timedelta, timezone
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from payload.api_response import SuccessApiResponse, ErrorApiResponse
from services.app.flight_service import FlightService

flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/search', methods=['GET'])
def search_flights():
    """Search flights with optional filters"""
    try:
        search_params = {
            'departureAirport': request.args.get('departureAirport'),
            'arrivalAirport': request.args.get('arrivalAirport'),
            'flightDate': request.args.get('flightDate')
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v}
        
        flights = FlightService.search_flights(search_params)
        
        return jsonify(SuccessApiResponse(data={
            'flights': flights,
            'total': len(flights)
        }).to_dict()), 200
        
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/', methods=['GET'])
def get_all_flights():
    """Get all flights"""
    try:
        flights = Flight.query.filter_by(status="ACTIVE").all()
        result = []

        for flight in flights:
            ticket_classes = FlightTicketClass.query.filter_by(flight_id=flight.id).all()
            ticket_data = []
            for t in ticket_classes:
                class_info = TicketClass.query.get(t.ticket_class_id)
                if class_info:
                    ticket_data.append({
                        "class_name": class_info.class_name,
                        "total_seats": t.total_seats
                    })

            intermediates = IntermediateAirport.query.filter_by(flight_id=flight.id).all()
            stops = []
            for i in intermediates:
                airport = Airport.query.get(i.intermediate_airport_id)
                if airport:
                    stops.append({
                        "airport_name": airport.airport_name,
                        "stop_duration": i.stop_duration,
                        "note": i.notes
                    })

            flight_data = flight.to_dict()
            flight_data["ticket_classes"] = ticket_data
            flight_data["intermediate_airports"] = stops
            result.append(flight_data)

        return jsonify(SuccessApiResponse(data=result).to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    """Get flight by ID"""
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify({"error": "Flight not found"}), 404

        ticket_classes = FlightTicketClass.query.filter_by(flight_id=flight.id).all()
        ticket_data = []
        for t in ticket_classes:
            class_info = TicketClass.query.get(t.ticket_class_id)
            if class_info:
                ticket_data.append({
                    "class_name": class_info.class_name,
                    "total_seats": t.total_seats
                })

        intermediates = IntermediateAirport.query.filter_by(flight_id=flight.id).all()
        stops = []
        for i in intermediates:
            airport = Airport.query.get(i.intermediate_airport_id)
            if airport:
                stops.append({
                    "airport_name": airport.airport_name,
                    "stop_duration": i.stop_duration,
                    "note": i.notes
                })

        result = flight.to_dict()
        result["ticket_classes"] = ticket_data
        result["intermediate_airports"] = stops

        return jsonify(SuccessApiResponse(data=result).to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

# PROTECTED - Authentication required
@flight_bp.route('/', methods=['POST'])
@jwt_required()
def create_flight():
    """Create flight - ADMIN ONLY"""
    try:
        data = request.json
        current_user = get_jwt_identity()  # You should add role check here

        from_airport = data.get("from_airport")
        to_airport = data.get("to_airport")
        departure_time = data.get("departure_time")
        flight_time_minutes = int(data.get("flight_time_minutes"))
        base_price = float(data.get("base_price"))
        stops = data.get("intermediate_airports", [])
        seat_config = data.get("seat_config", [])

        all_airport_ids = [a.id for a in Airport.query.all()]
        if from_airport not in all_airport_ids or to_airport not in all_airport_ids:
            return jsonify(ErrorApiResponse(message="Sân bay không tồn tại").to_dict()), 400
        if from_airport == to_airport:
            return jsonify(ErrorApiResponse(message="Sân bay đi và đến không được giống nhau").to_dict()), 400
        if flight_time_minutes < 30:
            return jsonify(ErrorApiResponse(message="Thời gian bay tối thiểu là 30 phút").to_dict()), 400
        if len(stops) > 2:
            return jsonify(ErrorApiResponse(message="Chỉ được tối đa 2 sân bay trung gian").to_dict()), 400

        for stop in stops:
            if stop['id'] in [from_airport, to_airport]:
                return jsonify(ErrorApiResponse(message="Sân bay trung gian không được trùng sân bay đi/đến").to_dict()), 400
            if not (10 <= stop['stop_duration'] <= 20):
                return jsonify(ErrorApiResponse(message="Thời gian dừng phải từ 10 đến 20 phút").to_dict()), 400

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
            inter = IntermediateAirport(
                flight_id=flight.id,
                intermediate_airport_id=stop['id'],
                stop_order=stop['stop_order'],
                stop_duration=stop['stop_duration'],
                notes=stop.get('note', ''),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(inter)

        for item in seat_config:
            seat = FlightTicketClass(
    flight_id=flight.id,
    ticket_class_id=item['ticket_class_id'],
    total_seats=item['total_seats'],
    available_seats=item.get('available_seats', item['total_seats']),
    ticket_price=item['ticket_price'],
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc)
)


            db.session.add(seat)

        db.session.commit()

        return jsonify(SuccessApiResponse(data={"flight_id": flight.id}).to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/airports', methods=['GET'])
def get_airports():
    try:
        airports = Airport.query.all()
        data = [{'id': a.id, 'airport_name': a.airport_name} for a in airports]
        return jsonify(SuccessApiResponse(data=data).to_dict()), 200
    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify(ErrorApiResponse(message="Flight not found").to_dict()), 404

        data = request.json

        from_airport = data.get("from_airport")
        to_airport = data.get("to_airport")
        departure_time = data.get("departure_time")
        flight_time_minutes = int(data.get("flight_time_minutes"))
        base_price = float(data.get("base_price"))
        stops = data.get("intermediate_airports", [])
        seat_config = data.get("seat_config", [])

        all_airport_ids = [a.id for a in Airport.query.all()]
        if from_airport not in all_airport_ids or to_airport not in all_airport_ids:
            return jsonify(ErrorApiResponse(message="Sân bay không tồn tại").to_dict()), 400
        if from_airport == to_airport:
            return jsonify(ErrorApiResponse(message="Sân bay đi và đến không được giống nhau").to_dict()), 400
        if flight_time_minutes < 30:
            return jsonify(ErrorApiResponse(message="Thời gian bay tối thiểu là 30 phút").to_dict()), 400
        if len(stops) > 2:
            return jsonify(ErrorApiResponse(message="Chỉ được tối đa 2 sân bay trung gian").to_dict()), 400

        for stop in stops:
            if stop['id'] in [from_airport, to_airport]:
                return jsonify(ErrorApiResponse(message="Sân bay trung gian không được trùng sân bay đi/đến").to_dict()), 400
            if not (10 <= stop['stop_duration'] <= 20):
                return jsonify(ErrorApiResponse(message="Thời gian dừng phải từ 10 đến 20 phút").to_dict()), 400

        # Cập nhật thông tin chuyến bay
        departure_dt = datetime.fromisoformat(departure_time)
        total_stop = sum([int(s['stop_duration']) for s in stops])
        arrival_time = departure_dt + timedelta(minutes=flight_time_minutes + total_stop)

        flight.departure_airport_id = from_airport
        flight.arrival_airport_id = to_airport
        flight.departure_time = departure_dt
        flight.arrival_time = arrival_time
        flight.flight_duration = flight_time_minutes
        flight.base_price = base_price
        flight.updated_at = datetime.now(timezone.utc)

        # Xoá sân bay trung gian cũ
        IntermediateAirport.query.filter_by(flight_id=flight.id).delete()

        for stop in stops:
            new_stop = IntermediateAirport(
                flight_id=flight.id,
                intermediate_airport_id=stop['id'],
                stop_order=stop['stop_order'],
                stop_duration=stop['stop_duration'],
                notes=stop.get('note', ''),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(new_stop)

        # Xoá cấu hình ghế cũ
        FlightTicketClass.query.filter_by(flight_id=flight.id).delete()

        for item in seat_config:
            seat = FlightTicketClass(
                flight_id=flight.id,
                ticket_class_id=item['ticket_class_id'],
                total_seats=item['total_seats'],
                available_seats=item.get('available_seats', item['total_seats']),
                ticket_price=item['ticket_price'],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(seat)

        db.session.commit()

        return jsonify(SuccessApiResponse(data={"flight_id": flight.id}).to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500

@flight_bp.route('/<int:flight_id>', methods=['DELETE'])
def cancel_flight(flight_id):
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify(ErrorApiResponse(message="Flight not found").to_dict()), 404

        # Nếu có vé thì chỉ đổi trạng thái
        flight.status = "CANCELLED"
        flight.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify(SuccessApiResponse(message="Đã huỷ chuyến bay").to_dict()), 200

    except Exception as e:
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500