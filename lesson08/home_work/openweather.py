
""" 
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""


from ow_appid import OpenWeatherAppId
from ow_cities import OpenWeatherCities
from ow_database import OpenWeatherDatabase
from ow_api import OpenWeatherApi


class OpenWeatherApp:
    def __init__(self):
        self.app_id = OpenWeatherAppId()
        self.cities = OpenWeatherCities()
        self.api = OpenWeatherApi()
        self.database = OpenWeatherDatabase()
        try:
            # пытаемся создать таблицы в БД
            self.database.create_tables()
        except:
            # если ecpetion, то ничего не делаем - таблицы уже есть
            pass

    def get_weather(self, cities_id):
        # получаем погоду и записываем в БД
        weather_data = self.api.get_data(cities_id, appid=self.app_id.get_app_id(), units="metric")
        self.database.add_weather(weather_data)
        return weather_data

    def menu(self):
        print("====================================")
        print("0. Выход")
        print("1. Получить список доступных стран")
        print("2. Поиск города")
        print("3. Погода в городе")
        print("====================================")

    def __cmd_halt(self):
        return True

    def __cmd_get_countries(self):
        print(app.cities.get_countries())
        return False

    def __cmd_get_cities(self):
        country = input("Введите страну: ")
        country = country.lower()
        if country not in map(lambda x: x.lower(), app.cities.get_countries()):
            print("Такой страны в базе нет")
            return False
        city_re = input("Введите первые буквы названия города: ")
        print(app.cities.get_cities(country, city_re))
        return False

    def __cmd_city_weather(self):
        country = input("Введите страну: ")
        if country.lower() not in map(lambda x: x.lower(), app.cities.get_countries()):
            print("Такой страны в базе нет")
            return False
        city = input("Введите название города: ")
        if city.lower() not in map(lambda x: x.lower(), app.cities.get_cities(country)):
            print("Такого города в БД для выбраноой нет")
            return False
        cities_id_list = self.cities.get_city_id(country, city)
        print(f"В укзанной стране найдено городов с таким названием: {len(cities_id_list)}")
        print("Запрашиваю погоду по всем...")
        data = self.get_weather(cities_id_list)
        if "cnt" in data.keys():
            for i in range(data["cnt"]):
                print(f"Город {data['list'][i]['name']}, t= {data['list'][i]['main']['temp']} °C")
        else:
            print(f"Город {data['name']}, t= {data['main']['temp']} C")
        print()

        return False

    def run(self):
        menu = {0: self.__cmd_halt,
                1: self.__cmd_get_countries,
                2: self.__cmd_get_cities,
                3: self.__cmd_city_weather}
        while True:
            try:
                self.menu()
                n = int(input("Введите операцию: "))
                if n not in menu.keys():
                    print("Такого пункта меню нет")
                    continue
            except Exception as e:
                print(f"Ошибка ввода {e}")
                continue

            if menu[n]():
                # вываливаемся если вренули True - только при 0
                break


try:
    app = OpenWeatherApp()
    app.run()
except Exception as e:
    print(e)
