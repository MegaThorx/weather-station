import requests

api_key = '2678fc5edec0fa22ba8f9d60b5085edc'
base_url = 'https://api.openweathermap.org/data/2.5/'
location = 'Innsbruck'


def get_current_weather():
    response = requests.get(base_url + 'weather?q=' + location + '&units=metric&appid=' + api_key)
    return response.json()


def get_forecast():
    response = requests.get(base_url + '/forecast?q=' + location + '&units=metric&appid=' + api_key)
    # return only the next 3 forecasts
    forecasts = [
        response.json()['list'][0],
        response.json()['list'][1],
        response.json()['list'][2]
    ]

    return forecasts