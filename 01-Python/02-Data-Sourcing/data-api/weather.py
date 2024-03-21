# pylint: disable=missing-module-docstring

import sys
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    """
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    """
    endpoint = "/geo/1.0/direct"
    params = {"q": query, "limit": 10}

    response = requests.get(f"{BASE_URI}{endpoint}", params=params)

    if response.status_code > 200:
        print("Something went wrong! Error code:", response.status_code)
        return None

    all_locations = response.json()
    n_locations = len(all_locations)

    # No matches
    if n_locations < 1:
        print("No location with this name found.")
        return None

    # Too many matches
    if n_locations > 1:
        print(f"Found {n_locations} matches!" "Select one of the following:")
        for idx, loc in enumerate(all_locations):
            print(f"{idx+1}. {loc['name']}, {loc['country']}")
        return all_locations[int(input("Location number: ")) - 1]

    # Simple case
    return all_locations[0]


def weather_forecast(lat, lon):
    """Return a 5-day weather forecast for the city, given its latitude and longitude."""

    endpoint = "/data/2.5/forecast"

    params = {"lat": lat, "lon": lon, "units": "metric", "cnt": 40}

    response = requests.get(f"{BASE_URI}{endpoint}", params=params)
    if response.status_code > 200:
        print("Something went wrong! Error code:", response.status_code)
    else:
        forecasts = response.json()["list"]

    five_day_forecast = {day["dt_txt"][:10]: day for day in forecasts[::-1]}

    return list(five_day_forecast.values())[::-1][1:]

def print_forcasts(forecasts):
    """Print the five day forcast."""
    for forecast in forecasts:
        date = forecast['dt_txt'][:10]
        weather = forecast['weather'][0]['main']
        temp = round(forecast['main']['temp'])
        print(
                f"{date}: {weather} ({temp}°C)"
            )

def main():
    """Ask user for a city and display weather forecast"""
    query = input("City?\n> ")
    city = search_city(query)
    lat, lon = city["lat"], city["lon"]
    print("Getting forcast for {city}")
    five_day_forecast = weather_forecast(lat, lon)
    print_forcasts(five_day_forecast)


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
