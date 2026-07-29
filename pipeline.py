import requests
import pandas as pd

from config import API_URL


def fetch_data():
    """
    Fetch live arrival data from the TfL API.
    Returns a list of dictionaries containing train arrivals.
    """

    try:
        # Send GET request to the API
        response = requests.get(API_URL)

        # Raise an error if the request failed
        response.raise_for_status()

        # Convert JSON response into Python objects
        data = response.json()

        return data

    except requests.exceptions.RequestException as error:
        print("Error connecting to the TfL API.")
        print(error)

        return []


def clean_data(data):
    """
    Extract only the information we need from the API response.
    Returns a Pandas DataFrame.
    """

    arrivals = []

    for train in data:

        line = train.get("lineName", "Unknown")

        destination = train.get("destinationName", "Unknown")

        minutes_away = round(train.get("timeToStation", 0) / 60)

        expected_arrival = train.get("expectedArrival", "Unknown")

        arrivals.append({
            "Line": line,
            "Destination": destination,
            "Minutes_Away": minutes_away,
            "Expected_Arrival": expected_arrival
        })

    dataframe = pd.DataFrame(arrivals)

    # Sort by the train arriving soonest
    dataframe = dataframe.sort_values("Minutes_Away")

    # Reset row numbers after sorting
    dataframe = dataframe.reset_index(drop=True)

    return dataframe

def get_arrivals():
    """
    Returns a cleaned DataFrame containing live arrivals.
    """

    raw_data = fetch_data()

    if len(raw_data) == 0:
        return pd.DataFrame()

    dataframe = clean_data(raw_data)

    return dataframe

def main():

    dataframe = get_arrivals()

    if dataframe.empty:
        print("No data received.")
    else:
        print(dataframe)


if __name__ == "__main__":
    main()