
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]
    
При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import sys
import csv
import json
from datetime import datetime
from ow_database import OpenWeatherDatabase

icons = {"01": [800	],
         "02": [801],
         "03": [802],
         "04": [803, 804],
         "09": [300, 301, 302, 310, 311, 312, 313, 314, 321, 520, 521, 522, 531],
         "10": [500, 501, 502, 503, 504],
         "11": [200, 201, 202, 210, 211, 212, 221, 230, 231, 232],
         "13": [511, 600, 601, 602, 611, 612, 615, 616, 620, 621, 622],
         "50": [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]}


class ExportOW:
    def __init__(self):
        self.database = OpenWeatherDatabase()

    @staticmethod
    def get_icon(weather_id):
        # Покажем картинку в зависимости от времени пользователя
        if 8 <= datetime.now().timetuple()[3] <= 20:
            day_night = "d"
        else:
            day_night = "n"
        for k in icons.keys():
            if weather_id in icons[k]:
                icon_url = f"http://openweathermap.org/img/w/{k}{day_night}.png"
                return icon_url

    def export_csv(self, filename, data):
        head = ["city_id", "city_name", "weather_date", "temperature", "weather_id"]
        with open(filename, 'w', newline='') as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            wr.writerow(head)
            for row in data:
                wr.writerow(row)

    def export_json(self, filename, data):
        head = ["city_id", "city_name", "weather_date", "temperature", "weather_id"]
        d = []
        for row in data:
            d.append(dict(list(zip(head, row))))

        with open(filename, 'w', newline='') as json_file:
            json_file.write(json.dumps(d))

    def export_html(self, filename, data):
        head = ["id", "Город", "Время последнего обновления", "Температура", "Визуализация"]
        with open(filename, 'w', newline='') as html_file:
            html_file.write("<html>")
            html_file.write("<head>")
            html_file.write("<title>Даннные о погоде</title>")
            html_file.write("</head>")
            html_file.write("<body>")
            html_file.write("<table border='1' cellspacing='0'>")
            html_file.write("<caption>Погода</caption>")
            html_file.write("<tr>")
            for item in head:
                html_file.write("<th>")
                html_file.write(item)
                html_file.write("</th>")
            html_file.write("</tr>")
            for row in data:
                html_file.write("<tr>")
                r = list(row)
                r.append(f"<img src='{self.get_icon(r.pop())}'>")
                for item in r:
                    html_file.write("<td>")
                    html_file.write(str(item))
                    html_file.write("</td>")
                html_file.write("</tr>")
            html_file.write("</table>")
            html_file.write("</body>")
            html_file.write("</html>")

    def run(self, param, filename, city_name):
        menu = {"--csv": self.export_csv,
                "--json": self.export_json,
                "--html": self.export_html}
        data = self.database.get_weather(city_name)
        if len(data) == 0:
            print("Погоды для указанного города не найдено")
        else:
            menu[param](filename, data)


def print_help():
    print("Для использования введите: ")
    print("export_openweather.py --csv filename [<город>]")
    print("export_openweather.py --json filename [<город>]")
    print("export_openweather.py --html filename [<город>]")


if len(sys.argv) < 3:
    print_help()
    sys.exit(0)

try:
    city = sys.argv[3]
except:
    city = None

eow = ExportOW()
eow.run(sys.argv[1], sys.argv[2], city)

