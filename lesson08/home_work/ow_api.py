import json
from urllib import request, parse


class OpenWeatherApi:
    def __init__(self):
        self.API_URL = "http://api.openweathermap.org/data/2.5"

    def get_data(self, *args, appid, units=None):
        function = "group" if len(args) > 1 else "weather"
        params = {}
        if len(args) == 1:
            params["id"] = args[0]
        else:
            args_str = ""
            for arg in args:
                args_str += str(arg) + ","
            params["id"] = args_str[:-1]
        if units:
            params["units"] = units
        params["appid"] = appid
        _url = f"{self.API_URL}/{function}?{parse.urlencode(params)}"
        response = request.urlopen(_url)
        data = response.read()

        return json.loads(data.decode("utf-8"))
