import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta

auth_api_url = "http://20.244.56.144/train/auth"
train_api_url = "http://20.244.56.144/train/trains"

data = {
    "companyName": "Train Central",
    "clientID": "ab5767e9-9d45-4826-8ecc-9e0851673e3d",
    "ownerName": "Sankarshan",
    "rollNo": "2004060",
    "ownerEmail": "2004060@kiit.ac.in",
    "clientSecret": "ranxGMNCcCdlEBYq"
}

app = Flask(__name__)

def get_train_details():
    try:
        auth_response = requests.post(auth_api_url, json=data)

        if auth_response.status_code == 200:
            access_token = auth_response.json().get("access_token")
            print("Access Token Obtained Successfully")
        else:
            # Access token request failed, print the error response
            print("Access Token Request Failed")
            print("Error Response:")
            print(auth_response.content)
            return None

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        train_response = requests.get(train_api_url, headers=headers)

        if train_response.status_code == 200:
            # Train details fetched successfully
            train_data = train_response.json()

            # Filter out trains with departure time more than 30 minutes and consider delay
            filtered_trains = []
            for train in train_data:
                departure_time = train.get("departureTime")
                delayed_by = train.get("delayedBy")

                if departure_time["Minutes"] <= 30 and delayed_by <= 30:
                    filtered_trains.append(train)

            # Sort filtered_trains first in ascending order based on 'price' (AC class)
            filtered_trains = sorted(filtered_trains, key=lambda x: x['price']['AC'])

            # Sort the same list in descending order based on available seats for AC class
            filtered_trains = sorted(filtered_trains, key=lambda x: x['seatsAvailable']['AC'], reverse=True)

            # Sort the same list in descending order based on departure time
            filtered_trains = sorted(filtered_trains, key=lambda x: x['departureTime']['Hours'], reverse=True)

            return filtered_trains

        else:
            # Train details request failed, print the error response
            print("Train Details Request Failed")
            print("Error Response:")
            print(train_response.content)
            return None

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        print("Request Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

@app.route('/trains', methods=['GET'])         
def get_trains():
    train_details = get_train_details()
    if train_details:
        return jsonify(train_details)
    else:
        return jsonify({"message": "Error fetching train details"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)

