from flask import Blueprint, request, jsonify
from models.flight_model import Flight
from models.ticket_class_model import TicketClass
from models.intermediate_airport_model import IntermediateAirport
from models.airport_model import Airport
from models.flight_ticket_class_model import FlightTicketClass
from payload.api_response import SuccessApiResponse
from datetime import datetime, timedelta
from app.extensions import db


flight_bp = Blueprint('flight', __name__)


@flight_bp.route('/airports', methods=['GET'])
def get_airports():
    try:
        airports = Airport.query.all()
        data = [{'id': a.id, 'airport_name': a.airport_name} for a in airports]
        return jsonify(SuccessApiResponse(data=data).to_dict()), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500




@flight_bp.route('/flights/create', methods=['POST'])
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


        all_airport_ids = [a.id for a in Airport.query.all()]
        if from_airport not in all_airport_ids or to_airport not in all_airport_ids:
            return jsonify({"error": "Sân bay không tồn tại"}), 400
        if from_airport == to_airport:
            return jsonify({"error": "Sân bay đi và đến không được giống nhau"}), 400
        if flight_time_minutes < 30:
            return jsonify({"error": "Thời gian bay tối thiểu là 30 phút"}), 400
        if len(stops) > 2:
            return jsonify({"error": "Chỉ được tối đa 2 sân bay trung gian"}), 400


        for stop in stops:
            if stop['id'] in [from_airport, to_airport]:
                return jsonify({"error": "Sân bay trung gian không được trùng sân bay đi/đến"}), 400
            if not (10 <= stop['stop_duration'] <= 20):
                return jsonify({"error": "Thời gian dừng phải từ 10 đến 20 phút"}), 400


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
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(inter)


        for item in seat_config:
            seat = FlightTicketClass(
                flight_id=flight.id,
                ticket_class_id=item['ticket_class_id'],
                total_seats=item['total_seats'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(seat)


        db.session.commit()


        return jsonify(SuccessApiResponse(data={"flight_id": flight.id}).to_dict()), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500




@flight_bp.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
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
        return jsonify({"error": str(e)}), 500




@flight_bp.route('/flights/search', methods=['GET'])
def search_flights():
    try:
        from_location = int(request.args.get('from'))
        to_location = int(request.args.get('to'))
        depart_date = request.args.get('departDate')


        if not depart_date:
            raise ValueError("Missing departDate")


        depart_day_start = datetime.strptime(depart_date, "%Y-%m-%d")
        depart_day_end = depart_day_start.replace(hour=23, minute=59, second=59)
    except Exception as e:
        return jsonify({"error": f"Missing or invalid parameters: from, to, departDate. {e}"}), 400


    flights = Flight.query.filter(
        Flight.departure_airport_id == from_location,
        Flight.arrival_airport_id == to_location,
        Flight.departure_time.between(depart_day_start, depart_day_end),
        Flight.status == "ACTIVE"
    ).all()


    results = []


    for f in flights:
        ticket_classes = TicketClass.query.filter_by(status='ACTIVE').all()
        ticket_prices = []
        for cls in ticket_classes:
            price = round(float(f.base_price) * float(cls.price_multiplier))
            ticket_prices.append({
                'class_name': cls.class_name,
                'price': price
            })


        intermediates = IntermediateAirport.query.filter_by(flight_id=f.id).all()
        stopovers = []
        for i in intermediates:
            if 10 <= i.stop_duration <= 20:
                airport = Airport.query.get(i.intermediate_airport_id)
                stopovers.append({
                    'name': airport.airport_name,
                    'stop_duration': i.stop_duration,
                    'note': i.notes
                })


        flight_data = f.to_dict()
        flight_data['ticket_classes'] = ticket_prices
        flight_data['intermediate_airports'] = stopovers


        results.append(flight_data)


    return jsonify(SuccessApiResponse(data=results).to_dict()), 200

@flight_bp.route('/flights', methods=['GET'])
def get_all_flights():
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
        return jsonify({"error": str(e)}), 500
    

@flight_bp.route('/flights/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify({"error": "Flight not found"}), 404

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
            return jsonify({"error": "Sân bay không tồn tại"}), 400
        if from_airport == to_airport:
            return jsonify({"error": "Sân bay đi và đến không được giống nhau"}), 400
        if flight_time_minutes < 30:
            return jsonify({"error": "Thời gian bay tối thiểu là 30 phút"}), 400
        if len(stops) > 2:
            return jsonify({"error": "Chỉ được tối đa 2 sân bay trung gian"}), 400

        for stop in stops:
            if stop['id'] in [from_airport, to_airport]:
                return jsonify({"error": "Sân bay trung gian không được trùng sân bay đi/đến"}), 400
            if not (10 <= stop['stop_duration'] <= 20):
                return jsonify({"error": "Thời gian dừng phải từ 10 đến 20 phút"}), 400

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
        flight.updated_at = datetime.utcnow()

        # Xoá sân bay trung gian cũ
        IntermediateAirport.query.filter_by(flight_id=flight.id).delete()

        for stop in stops:
            new_stop = IntermediateAirport(
                flight_id=flight.id,
                intermediate_airport_id=stop['id'],
                stop_order=stop['stop_order'],
                stop_duration=stop['stop_duration'],
                notes=stop.get('note', ''),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_stop)

        # Xoá cấu hình ghế cũ
        FlightTicketClass.query.filter_by(flight_id=flight.id).delete()

        for item in seat_config:
            seat = FlightTicketClass(
    flight_id=flight.id,
    ticket_class_id=item['ticket_class_id'],
    total_seats=item['total_seats'],
    available_seats=item.get('available_seats', item['total_seats']),  # mặc định bằng total_seats nếu không truyền
    ticket_price=item['ticket_price'],  # PHẢI có dòng này!
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

            db.session.add(seat)

        db.session.commit()

        return jsonify(SuccessApiResponse(data={"flight_id": flight.id}).to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@flight_bp.route('/flights/<int:flight_id>', methods=['DELETE'])
def cancel_flight(flight_id):
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify({"error": "Flight not found"}), 404

        # Nếu có vé thì chỉ đổi trạng thái
        flight.status = "CANCELLED"
        flight.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
    "success": True,
    "message": "Đã huỷ chuyến bay",
    "data": None
}), 200



    except Exception as e:
        return jsonify({"error": str(e)}), 500






