import requests


class WeatherBit:
    """
    Class realize interaction with api weatherbit.io
    """

    def __init__(self, token):
        self.token = token
        self.url = 'https://api.weatherbit.io/v2.0/'

    def get_current_weather(self, user, _method='current?'):
        """

        :param user: User obj
        :param _method: API method, don't change
        :return: info about current weather
        """
        params = {
            'city': user.city,
            'lang': user.lang,
        }
        response = requests.get(self.url + _method + f'key={self.token}', params=params)
        return response.json()['data'][0]

    def get_tomorrow_weather(self, user, hours='24', _method='forecast/hourly?'):

        params ={
            'city': user.city,
            'lang': user.lang,
            'hours': hours,
        }

        response = requests.get(self.url + _method + f'key={self.token}', params=params)
        return response.json()

    def get_weather_week(self, user, days='7', _method='forecast/daily?'):

        params = {
            'city': user.city,
            'lang': user.lang,
            'days': days,
        }
        response = requests.get(self.url + _method + f'key={self.token}', params=params)
        return response.json()

    @classmethod
    def check_city(cls, city, token):
        """
        :param city: name city
        :param token: API token for WeatherBit
        if city not exits status code will be 204 but status code is 200 this city exist
        """
        params = {
            'city': city
        }
        response = requests.get('https://api.weatherbit.io/v2.0/current?' + f'key=0e8af887b2ec48f589c6bea484554331', params=params)

        if response.status_code == 200:
            return True

