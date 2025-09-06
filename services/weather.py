import requests
from decouple import config

def get_weather(cidade):
    DIAS = 2
    URL = f"http://api.weatherapi.com/v1/forecast.json?key={config('WEATHER_API')}&q={cidade}&days={DIAS}&aqi=no&alerts=no&lang=pt"
    return requests.get(URL)

