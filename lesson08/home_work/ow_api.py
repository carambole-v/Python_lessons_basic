import json
from urllib import request, parse


class OpenWeatherApi:
    def __init__(self):
        self.API_URL = "http://api.openweathermap.org/data/2.5"

    def get_data(self, city_list, appid, units=None):
        params = {}
        if len(city_list) < 1:
            return dict()
        elif len(city_list) == 1:
            function = "weather"
            params["id"] = city_list[0]
        else:
            function = "group"
            cities_str = ""
            for city in city_list:
                cities_str += str(city) + ","
            params["id"] = cities_str[:-1]
        if units:
            params["units"] = units
        params["appid"] = appid
        _url = f"{self.API_URL}/{function}?{parse.urlencode(params)}"
        response = request.urlopen(_url)
        data = response.read()

        return json.loads(data.decode("utf-8"))
