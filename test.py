from app.app import app
from app.extensions import db
from models.flight_model import Flight
from models.airport_model import Airport

def test_database_connection():
    """Test basic database connection"""
    with app.app_context():
        try:
            # Test if tables exist
            result = db.engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [row[0] for row in result]
            print(f"✅ Found tables: {tables}")
            return True
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False

def test_airport_queries():
    """Test Airport model queries"""
    with app.app_context():
        try:
            # Test SELECT all airports
            airports = Airport.query.all()
            print(f"\n🛫 Total Airports: {len(airports)}")
            
            for airport in airports:
                print(f"  - ID: {airport.id}, Name: {airport.airport_name}, Status: {airport.status}")
            
            # Test SELECT by ID
            if airports:
                first_airport = Airport.query.filter_by(id=airports[0].id).first()
                print(f"\n📍 First Airport Details: {first_airport.to_dict()}")
            
            # Test SELECT with LIKE
            search_airports = Airport.query.filter(Airport.airport_name.ilike('%Hồ Chí Minh%')).all()
            print(f"\n🔍 Airports containing 'Hồ Chí Minh': {len(search_airports)}")
            
        except Exception as e:
            print(f"❌ Airport query error: {e}")

def test_flight_queries():
    """Test Flight model queries"""
    with app.app_context():
        try:
            # Test SELECT all flights
            flights = Flight.query.all()
            print(f"\n✈️ Total Flights: {len(flights)}")
            
            for flight in flights:
                print(f"  - Flight ID: {flight.id}")
                print(f"    From: {flight.departure_airport_id} To: {flight.arrival_airport_id}")
                print(f"    Departure: {flight.departure_time}")
                print(f"    Duration: {flight.flight_duration} minutes")
                print(f"    Price: {flight.base_price}")
                print(f"    Status: {flight.status}")
                print("---")
            
            # Test SELECT with JOIN
            flights_with_airports = db.session.query(Flight).join(
                Airport, Flight.departure_airport_id == Airport.id
            ).all()
            print(f"\n🔗 Flights with Airport JOIN: {len(flights_with_airports)}")
            
            # Test flight.to_dict() method
            if flights:
                flight_dict = flights[0].to_dict()
                print(f"\n📊 First Flight as Dict: {flight_dict}")
                
        except Exception as e:
            print(f"❌ Flight query error: {e}")

def test_relationship_queries():
    """Test model relationships"""
    with app.app_context():
        try:
            # Test accessing relationships
            flights = Flight.query.all()
            for flight in flights:
                print(f"\n✈️ Flight {flight.id}:")
                
                # Access departure airport via relationship
                if flight.departure_airport:
                    print(f"  Departure: {flight.departure_airport.airport_name}")
                else:
                    print(f"  Departure Airport ID: {flight.departure_airport_id} (No relationship data)")
                
                # Access arrival airport via relationship  
                if flight.arrival_airport:
                    print(f"  Arrival: {flight.arrival_airport.airport_name}")
                else:
                    print(f"  Arrival Airport ID: {flight.arrival_airport_id} (No relationship data)")
                    
        except Exception as e:
            print(f"❌ Relationship query error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Model Tests...")
    
    # Test 1: Database connection
    if test_database_connection():
        # Test 2: Airport queries
        test_airport_queries()
        
        # Test 3: Flight queries  
        test_flight_queries()
        
        # Test 4: Relationship queries
        test_relationship_queries()
        
    print("\n🎉 Model testing completed!")