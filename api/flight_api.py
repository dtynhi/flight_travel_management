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
from services.app.system_parameter_service import SystemParameterService
from services.app.ticket_class_service import TicketClassService

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

# Update the PATCH function to use system parameters
@flight_bp.route('/<int:flight_id>', methods=['PUT'])
@jwt_required()
def update_flight_partial(flight_id):
    """Update specific fields of a flight - ADMIN ONLY"""
    try:
        flight = Flight.query.get(flight_id)
        if not flight:
            return jsonify(ErrorApiResponse(message="Flight not found").to_dict()), 404

        data = request.json
        current_user = get_jwt_identity()
        
        # Get system parameters for validation
        try:
            system_params = SystemParameterService.get_current_parameters()
        except:
            system_params = {
                'minimum_flight_duration': 30,
                'max_intermediate_stops': 2,
                'minimum_stop_duration': 10,
                'maximum_stop_duration': 20
            }
        
        # Track what was updated
        updated_fields = []

        # Update departure airport
        if 'from_airport' in data:
            new_from_airport = data['from_airport']
            all_airport_ids = [a.id for a in Airport.query.all()]
            if new_from_airport not in all_airport_ids:
                return jsonify(ErrorApiResponse(message="Sân bay đi không tồn tại").to_dict()), 400
            if new_from_airport == flight.arrival_airport_id:
                return jsonify(ErrorApiResponse(message="Sân bay đi không được trùng sân bay đến").to_dict()), 400
            flight.departure_airport_id = new_from_airport
            updated_fields.append("departure_airport")

        # Update arrival airport
        if 'to_airport' in data:
            new_to_airport = data['to_airport']
            all_airport_ids = [a.id for a in Airport.query.all()]
            if new_to_airport not in all_airport_ids:
                return jsonify(ErrorApiResponse(message="Sân bay đến không tồn tại").to_dict()), 400
            if new_to_airport == flight.departure_airport_id:
                return jsonify(ErrorApiResponse(message="Sân bay đến không được trùng sân bay đi").to_dict()), 400
            flight.arrival_airport_id = new_to_airport
            updated_fields.append("arrival_airport")

        # Update departure time
        if 'departure_time' in data:
            try:
                departure_dt = datetime.fromisoformat(data['departure_time'])
                flight.departure_time = departure_dt
                if flight.flight_duration:
                    stops = IntermediateAirport.query.filter_by(flight_id=flight.id).all()
                    total_stop = sum([s.stop_duration for s in stops])
                    flight.arrival_time = departure_dt + timedelta(minutes=flight.flight_duration + total_stop)
                updated_fields.append("departure_time")
            except ValueError:
                return jsonify(ErrorApiResponse(message="Định dạng thời gian không hợp lệ").to_dict()), 400

        # Update flight duration using system parameters
        if 'flight_time_minutes' in data:
            flight_time_minutes = int(data['flight_time_minutes'])
            min_flight_duration = system_params.get('minimum_flight_duration')
            if flight_time_minutes < min_flight_duration:
                return jsonify(ErrorApiResponse(message=f"Thời gian bay tối thiểu là {min_flight_duration} phút").to_dict()), 400
            flight.flight_duration = flight_time_minutes
            if flight.departure_time:
                stops = IntermediateAirport.query.filter_by(flight_id=flight.id).all()
                total_stop = sum([s.stop_duration for s in stops])
                flight.arrival_time = flight.departure_time + timedelta(minutes=flight_time_minutes + total_stop)
            updated_fields.append("flight_duration")

        # Update base price
        if 'base_price' in data:
            try:
                old_base_price = flight.base_price
                new_base_price = float(data['base_price'])
                flight.base_price = new_base_price
                
                # Update all existing flight ticket class prices when base price changes
                existing_flight_ticket_classes = FlightTicketClass.query.filter_by(flight_id=flight.id).all()
                print(existing_flight_ticket_classes)
                for ftc in existing_flight_ticket_classes:
                    # Get the ticket class data to access price_multiplier
                    try:
                        ticket_class_data = TicketClassService.get_ticket_class_by_id(ftc.ticket_class_id)
                        # Recalculate ticket price with new base price
                        ftc.ticket_price = new_base_price * float(ticket_class_data['priceMultiplier'])
                        ftc.updated_at = datetime.now(timezone.utc)
                    except Exception as e:
                        # Log error but continue with other ticket classes
                        print(f"Error updating ticket price for class {ftc.ticket_class_id}: {str(e)}")
                
                updated_fields.append("base_price")
                updated_fields.append("ticket_prices")  # Indicate that ticket prices were also updated
                
            except ValueError:
                return jsonify(ErrorApiResponse(message="Giá cơ bản không hợp lệ").to_dict()), 400

        # Update status
        if 'status' in data:
            valid_statuses = ['ACTIVE', 'CANCELLED', 'SCHEDULED']
            if data['status'] not in valid_statuses:
                return jsonify(ErrorApiResponse(message=f"Trạng thái không hợp lệ. Chỉ chấp nhận: {', '.join(valid_statuses)}").to_dict()), 400
            flight.status = data['status']
            updated_fields.append("status")

        # Update intermediate airports using system parameters
        if 'intermediate_airports' in data:
            stops = data['intermediate_airports']
            max_stops = system_params.get('max_intermediate_stops', 2)
            if len(stops) > max_stops:
                return jsonify(ErrorApiResponse(message=f"Chỉ được tối đa {max_stops} sân bay trung gian").to_dict()), 400
            
            min_stop_duration = system_params.get('minimum_stop_duration', 10)
            max_stop_duration = system_params.get('maximum_stop_duration', 20)
            
            # Validate stops
            for stop in stops:
                if stop['id'] in [flight.departure_airport_id, flight.arrival_airport_id]:
                    return jsonify(ErrorApiResponse(message="Sân bay trung gian không được trùng sân bay đi/đến").to_dict()), 400
                if not (min_stop_duration <= stop['stop_duration'] <= max_stop_duration):
                    return jsonify(ErrorApiResponse(message=f"Thời gian dừng phải từ {min_stop_duration} đến {max_stop_duration} phút").to_dict()), 400

            # Delete old intermediate airports
            IntermediateAirport.query.filter_by(flight_id=flight.id).delete()
            
            # Add new intermediate airports
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
            
            # Recalculate arrival time with new stops
            if flight.departure_time and flight.flight_duration:
                total_stop = sum([s['stop_duration'] for s in stops])
                flight.arrival_time = flight.departure_time + timedelta(minutes=flight.flight_duration + total_stop)
            
            updated_fields.append("intermediate_airports")

        # Update seat configuration (if provided)
        if 'seat_config' in data:
            print("Updating seat configuration")
            seat_config = data['seat_config']
            

                    
            for item in seat_config:
                if 'ticket_class_id' not in item:
                    return jsonify(ErrorApiResponse(message="ticket_class_id is required for seat configuration").to_dict()), 400
                
                try:
                    # Check if ticket class exists using your service
                    ticket_class_data = TicketClassService.get_ticket_class_by_id(item['ticket_class_id'])
                except:
                    return jsonify(ErrorApiResponse(message=f"Ticket class with ID {item['ticket_class_id']} not found").to_dict()), 400
                
                if 'total_seats' not in item or item['total_seats'] <= 0:
                    return jsonify(ErrorApiResponse(message="total_seats must be greater than 0").to_dict()), 400
            
            # Delete old seat configuration
            FlightTicketClass.query.filter_by(flight_id=flight.id).delete()

            # Add new seat configuration
            for item in seat_config:
                # Get ticket class data to access price_multiplier
                ticket_class_data = TicketClassService.get_ticket_class_by_id(item['ticket_class_id'])
                
                # Calculate ticket price based on flight's base_price x ticket class price_multiplier
                calculated_ticket_price = float(flight.base_price) * float(ticket_class_data['priceMultiplier'])
                
                seat = FlightTicketClass(
                    flight_id=flight.id,
                    ticket_class_id=item['ticket_class_id'],
                    total_seats=item['total_seats'],
                    available_seats=item.get('available_seats', item['total_seats']),
                    ticket_price=calculated_ticket_price,  # Use calculated price instead of manual input
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                db.session.add(seat)
            
            updated_fields.append("seat_configuration")

        # Update timestamp
        flight.updated_at = datetime.now(timezone.utc)

        # Commit changes
        db.session.commit()

        return jsonify(SuccessApiResponse(data={
            "flight_id": flight.id,
            "updated_fields": updated_fields,
            "message": f"Đã cập nhật {len(updated_fields)} trường dữ liệu",
            "applied_constraints": {
                "minimum_flight_duration": system_params.get('minimum_flight_duration', 30),
                "max_intermediate_stops": system_params.get('max_intermediate_stops', 2),
                "stop_duration_range": f"{system_params.get('minimum_stop_duration', 10)}-{system_params.get('maximum_stop_duration', 20)} minutes"
            }
        }).to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(ErrorApiResponse(message=str(e)).to_dict()), 500
    
    
@flight_bp.route('/', methods=['GET'])
def get_all_flights():
    """Get all flights"""
    try:
        flights = Flight.query.all()
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
