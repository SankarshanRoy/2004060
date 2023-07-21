import requests

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
            exit()  

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        train_response = requests.get(train_api_url, headers=headers)

        if train_response.status_code == 200:
            # Train details fetched successfully
            train_data = train_response.json()

            filtered_trains = []
            for train in train_data:
                departure_time = train.get("departureTime")
                delayed_by = train.get("delayedBy")

                if departure_time["Minutes"] <= 30 and delayed_by <= 30: # 
                    filtered_trains.append(train)

            # Sort filtered_trains first in ascending order based on 'price' (AC class)
            filtered_trains = sorted(filtered_trains, key=lambda x: x['price']['AC'])

            # Sort the same list in descending order based on available seats for AC class
            filtered_trains = sorted(filtered_trains, key=lambda x: x['seatsAvailable']['AC'], reverse=True)

            # Sort the same list in descending order based on departure time
            filtered_trains = sorted(filtered_trains, key=lambda x: x['departureTime']['Hours'], reverse=True)

            print("Train Details:")
            for train in filtered_trains:
                train_name = train.get("trainName")
                train_number = train.get("trainNumber")
                departure_time = train.get("departureTime")
                seats_available = train.get("seatsAvailable")
                prices = train.get("price")
                delayed_by = train.get("delayedBy")

                print(f"Train Name: {train_name}")
                print(f"Train Number: {train_number}")
                print(f"Departure Time: {departure_time['Hours']}:{departure_time['Minutes']}")
                print(f"Seats Available - Sleeper: {seats_available['sleeper']}, AC: {seats_available['AC']}")
                print(f"Prices - Sleeper: {prices['sleeper']}, AC: {prices['AC']}")
                print(f"Delayed By: {delayed_by} minutes")
                print()

        else:
            print("Train Details Request Failed")
            print("Error Response:")
            print(train_response.content)  

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        print("Request Error:", e)
    except Exception as e:
        print("Error:", e)

get_train_details()

