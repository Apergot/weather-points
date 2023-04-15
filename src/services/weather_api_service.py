import os
import requests


class WeatherApiService:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = 'https://api.weatherapi.com/v1'

    def search_interest_point(self, q):
        url = f'{self.base_url}/search.json'
        params = {'q': q, 'key': self.api_key}
        response = requests.get(url, params=params)

        if response.ok:
            content = response.json()
            return content[0] if len(content) > 0 else None
        else:
            return None

    def get_current_and_next_day_forecasts(self, q):
        url = f'{self.base_url}/forecast.json'
        params = {'q': q, 'key': self.api_key, 'days': 2}
        response = requests.get(url, params=params)

        if response.ok:
            return response.json()['forecast']['forecastday']
        else:
            return None



