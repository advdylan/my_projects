import requests
import sys
import json
from geopy.geocoders import Nominatim
from tabulate import tabulate

def main():
  
    city = input("City: ").capitalize()

    try:
        days = int(input("Days: "))
    except(ValueError):
        sys.exit("Wrong number of days")

    # Passing the name of the city to get_cords function that returns it's location as latitude and longitude that represent the coordinates at geographic coordinate system
    latitude,longitude = get_cords(city)

    # Passing all the required infomation to generate a link for Open-Meteo to send back json file
    link = link_generator(latitude,longitude,days)

 
    call = requests.get(link)
    o = call.json()
    time = o['hourly']['time']
    temperature = o['hourly']['temperature_2m']
    rain = o['hourly']['rain']
    day = format_date(time)

    weather_dict = {day[i]: [temperature[i], rain[i]] for i in range(len(day))}
    print(tabulate([(k, *v) for k, v in weather_dict.items()], headers=['Day', 'Temperature', 'Rain']))
    

def get_cords(city):
    """
    This function takes user input of city to get it's localization for open-meteo service
    """

    geolocator = Nominatim(user_agent="myapplication")
    location = geolocator.geocode(city)
    latitude = round(float(location.latitude), 2)
    longitude = round(float(location.longitude), 2)

    return latitude,longitude

def link_generator(latitude,longitude,days):
    """
    Using generated cords of user city, this function creates link for Open-Meteo API
    """
    link = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain&timezone=auto&forecast_days={days}'
    return link

def format_date(time):
    """
    Functions that clear output of open-meteo API to make data user friendly
    """
    new_time = []
    for day in time:
        new_day = day.replace("T",": ")
        new_time.append(new_day)  
    return new_time

        
if __name__ == "__main__":
    main()
