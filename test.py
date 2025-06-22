import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Login first and check the response
login_data = {
    "email": "duylw25@gmail.com",
    "password": "Abcd1234."
}

print("Attempting login...")
response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)

print("Login Status Code:", response.status_code)
print("Login Response Text:", response.text)

# Try to parse JSON if possible
try:
    login_json = response.json()
    print("Login Response JSON:", json.dumps(login_json, indent=2))
    
    # Check if login was successful
    if response.status_code == 200:
        # Try different possible token locations
        token = None
        if login_json and 'data' in login_json:
            if 'token' in login_json['data']:
                token = login_json['data']['token']
            elif 'access_token' in login_json['data']:
                token = login_json['data']['access_token']
        elif login_json and 'token' in login_json:
            token = login_json['token']
        elif login_json and 'access_token' in login_json:
            token = login_json['access_token']
        
        if token:
            print(f"\nToken found: {token}")
            
            # 2. Create flight
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            flight_data = {
                "from_airport": 1,
                "to_airport": 2,
                "departure_time": "2025-06-25T08:00:00",
                "flight_time_minutes": 120,
                "base_price": 1500000,
                "seat_config": [
                    {
                        "ticket_class_id": 1,
                        "total_seats": 20
                    }
                ]
            }

            print("\nCreating flight...")
            flight_response = requests.post(f"{BASE_URL}/api/v1/flight/", json=flight_data, headers=headers)
            print("Flight Status Code:", flight_response.status_code)
            print("Flight Response:", flight_response.json())
        else:
            print("Token not found in response!")
    else:
        print("Login failed!")
        
except json.JSONDecodeError:
    print("Response is not valid JSON")
except Exception as e:
    print(f"Error: {e}")