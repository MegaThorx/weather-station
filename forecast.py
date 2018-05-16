import json
import requests


def get_current_weather():
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Innsbruck&units=metric&appid=2678fc5edec0fa22ba8f9d60b5085edc')
    return response.json()['main']['temp']


def get_forecast():
    response = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=Innsbruck&units=metric&appid=2678fc5edec0fa22ba8f9d60b5085edc')
    # return only the next 3 forecasts
    print(response.json()['list'].get(0))