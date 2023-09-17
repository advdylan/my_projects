import requests
import sys
import json
from geopy.geocoders import Nominatim
from tabulate import tabulate

def main():
    city = input("City: ").capitalize()
    days = input("Days: ")

    latitude,longitude = get_cords(city)
    link = link_generator(latitude,longitude,days)

    call = requests.get(link)
    o = call.json()
    time = o['hourly']['time']
    temperature = o['hourly']['temperature_2m']
    rain = o['hourly']['rain']
    day = format_date(time)
    data = dict(zip(day, zip(temperature, rain)))
    headers = data.keys()
    
    #print(tabulate(rows, tablefmt="grid"))
    

def get_cords(city):
    geolocator = Nominatim(user_agent="myapplication")
    location = geolocator.geocode(city)
    latitude = round(float(location.latitude), 2)
    longitude = round(float(location.longitude), 2)

    return latitude,longitude

def link_generator(latitude,longitude,days):
    link = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain&timezone=auto&forecast_days={days}'
    return link

def format_date(time):
    new_time = []
    for day in time:
        new_day = day.replace("T",":")
        new_time.append(new_day)  
    return new_time
        
if __name__ == "__main__":
    main()



    #print(day)
    #print(time[0], temperature[0])
    #res = {time[i]: temperature[i] for i in range(len(time))}
    #for temp, date in res.items():
        #print(f"{temp}: {date}")