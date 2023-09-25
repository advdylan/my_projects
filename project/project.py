"""
This script fetches weather data for a given city and number of days from Open-Meteo API.
It uses geopy to get the coordinates of the city and tabulate to print the data in a tabular format.
"""

import requests
import json
from geopy.geocoders import Nominatim
from tabulate import tabulate

def main():
    city = input("City: ").capitalize()
    while not city:
        print("City name cannot be empty.")
        city = input("City: ").capitalize()

    days = input("Days: ")
    while not days.isdigit():
        print("Invalid number of days. Please enter a valid number.")
        days = input("Days: ")

    # Passing the name of the city to get_cords function that returns it's location as latitude and longitude that represent the coordinates
    latitude, longitude = get_cords(city)

    # Passing all the required infomation to generate a link for Open-Meteo to send back json file
    link = link_generator(latitude, longitude, int(days))

    try:
        call = requests.get(link)
        call.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    weather_data = call.json()
    print_weather_data(weather_data)

def get_cords(city):
    """
    This function takes user input of city to get it's localization for open-meteo service
    """
    geolocator = Nominatim(user_agent="myapplication")
    location = geolocator.geocode(city)
    latitude = round(float(location.latitude), 2)
    longitude = round(float(location.longitude), 2)

    return latitude, longitude

def link_generator(latitude, longitude, days):
    """
    Using generated cords of user city, this function creates link for Open-Meteo API
    """

    link = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain&timezone=auto&forecast_days={days}'
    return link

def format_date(time):
    """
    Functions that clear output of open-meteo API to make data user friendly
    """
    new_time = [day.replace("T", ": ") for day in time]
    return new_time

def print_weather_data(weather_data):
    time = weather_data['hourly']['time']
    temperature = weather_data['hourly']['temperature_2m']
    rain = weather_data['hourly']['rain']
    day = format_date(time)

    weather_dict = {day[i]: [temperature[i], rain[i]] for i in range(len(day))}
    print(tabulate([(k, *v) for k, v in weather_dict.items()], headers=['Day', 'Temperature', 'Rain'], tablefmt="grid"))

if __name__ == "__main__":
    main()
