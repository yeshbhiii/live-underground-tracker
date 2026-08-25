import requests
import pandas as pd

from config import BASE_URL


def fetch_data(station_id):

    url = f"{BASE_URL}/{station_id}/Arrivals"

    try:

        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        print(error)

        return []


def clean_data(data):

    arrivals = []

    for train in data:

        arrivals.append({

            "Line": train.get("lineName", "Unknown"),

            "Destination": train.get("destinationName", "Unknown"),

            "Minutes_Away": round(
                train.get("timeToStation", 0) / 60
            ),

            "Expected_Arrival": train.get(
                "expectedArrival",
                "Unknown"
            )

        })

    df = pd.DataFrame(arrivals)

    df = df.sort_values(
        "Minutes_Away"
    ).reset_index(drop=True)

    return df


def get_arrivals(station_id):

    data = fetch_data(station_id)

    if len(data) == 0:
        return pd.DataFrame()

    return clean_data(data)