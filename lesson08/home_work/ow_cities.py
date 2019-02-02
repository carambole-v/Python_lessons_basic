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
        print(f"Загружаю список городов {WWW}. Пожалуйста подождите...")
        try:
            response = request.urlopen(CITIES_URL)
            data = response.read()
            j = gzip.decompress(data).decode("utf-8")
            with open(CITIES_FILENAME, "w", encoding="utf-8") as f:
                f.write(j)
            self.clear()
            self.extend(json.loads(j))
            print("Список городов успешно загружен.")
        except Exception as e:
            raise Exception(f"Ошибка при загрузке списка с {WWW}: {e}")

    def load(self):
        try:
            print(f"Загружаю список городов из файла {CITIES_FILENAME}...")
            with open(CITIES_FILENAME, "r", encoding="utf-8") as f:
                j = f.read()
                self.clear()
                self.extend(json.loads(j))
            print(f"Города загружены")
        except FileNotFoundError:
            print(f"Файл {CITIES_FILENAME} не найден.")
            self.update()
        except Exception as e:
            raise Exception(f"Ошибка при загрузке городов из файла: {e}")

    def get_countries(self):
        countries = set()
        for city in self:
            countries.add(city["country"])
        countries.remove("")

        return list(countries)

    def get_cities(self, country, city_re=""):
        cities = []
        for city in self:
            if (city["country"].lower() == country.lower()) and (re.match(city_re.lower(), city["name"].lower())):
                cities.append(city["name"])

        return cities

    def get_city_id(self, country, city_name):
        # возвращает списко id городов по названию (может быть несколько)
        cities = []
        for city in self:
            if (city["country"].lower() == country.lower()) and (city["name"].lower() == city_name.lower()):
                cities.append(city["id"])

        return cities


