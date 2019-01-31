import json
import gzip
import re
from urllib import request, parse

CITIES_FILENAME = "cities.json"
CITIES_URL = "http://bulk.openweathermap.org/sample/city.list.json.gz"
WWW = "openweathermap.org"


class OpenWeatherCities(list):
    """
    Класс подтягивает и хранит список городов с openweathermap.org
    """
    def __init__(self):
        super().__init__()
        self.load()

    def update(self):
        print(f"Loading cities list from {WWW}. Please wait...")
        try:
            response = request.urlopen(CITIES_URL)
            data = response.read()
            j = gzip.decompress(data).decode("utf-8")
            with open(CITIES_FILENAME, "w", encoding="utf-8") as f:
                f.write(j)
            self.clear()
            self.extend(json.loads(j))
            print("Cities loaded successfully.")
        except Exception as e:
            raise Exception(f"Exception in loading cities from {WWW}: {e}")

    def load(self):
        try:
            print(f"Try load cities from {CITIES_FILENAME}...")
            with open(CITIES_FILENAME, "r", encoding="utf-8") as f:
                j = f.read()
                self.clear()
                self.extend(json.loads(j))
            print(f"Cities loaded successfully")
        except FileNotFoundError:
            print(f"File {CITIES_FILENAME} not found.")
            self.update()
        except Exception as e:
            raise Exception(f"Exception in load cities from file: {e}")

    def get_countries(self):
        countries = set()
        for city in self:
            countries.add(city["country"])
        countries.remove("")

        return list(countries)

    def get_cities(self, country, city_re=""):
        cities = []
        for city in self:
            if (city["country"] == country) and (re.match(city_re.lower(), city["name"].lower())):
                cities.append((city["id"], city["name"]))

        return cities


