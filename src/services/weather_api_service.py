import os
import requests


class WeatherApiService:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = 'https://api.weatherapi.com/v1'

    def search_interest_point(self, q):
        url = f'{self.base_url}/current.json'
        params = {'q': q, 'key': self.api_key}
        response = requests.get(url, params=params)

        if response.ok:
            return response.json()['location']
        else:
            return None



