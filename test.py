from app.app import app
from app.extensions import db
from models.airport_model import Airport

def debug_airport_status():
    with app.app_context():
        try:
            # Check all airports regardless of status
            all_airports = db.session.query(Airport).all()
            print(f"Total airports in DB: {len(all_airports)}")
            
            if all_airports:
                print("\nAirport statuses:")
                for airport in all_airports:
                    print(f"  ID {airport.id}: {airport.airport_name} - Status: '{airport.status}'")
            
            # Check what find_all() returns
            filtered_airports = db.session.query(Airport).filter(
                db.or_(Airport.status == 'ACTIVE', Airport.status.is_(None))
            ).all()
            print(f"\nFiltered airports (ACTIVE or NULL): {len(filtered_airports)}")
            
            # Check different status values
            active_count = db.session.query(Airport).filter(Airport.status == 'ACTIVE').count()
            null_count = db.session.query(Airport).filter(Airport.status.is_(None)).count()
            
            print(f"ACTIVE airports: {active_count}")
            print(f"NULL status airports: {null_count}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_airport_status()