# Класс работы с базой данных погоды

import sqlite3
from datetime import datetime

DATABASE_FILENAME = "weather.sqlite"


class OpenWeatherDatabase:
    """
    Взаимодействие с базой данных
    """
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILENAME)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_tables(self):
        sql = """
                 CREATE TABLE ow_cities 
                     (city_id integer primary key,
                      city_name text,
                      country text,
                      lon float,
                      lat float)
              """
        self.cursor.execute(sql)

        sql = """
                 CREATE TABLE ow_weather 
                     (city_id integer primary key,
                      city_name text,
                      weather_date datetime,
                      temperature float,
                      weather_id integer)
              """
        self.cursor.execute(sql)

    @staticmethod
    def sysdate(timestamp):
        # работаем с utc, т.к.: "Time of data calculation, unix, UTC"
        return datetime.utcfromtimestamp(timestamp)

    def add_weather(self, data):
        # сохраняемся в БД
        if "cnt" in data.keys():
            for i in range(data["cnt"]):
                try:
                    self.__insert_weather(data["list"][i])
                except sqlite3.IntegrityError:
                    self.__update_weather(data["list"][i])
        else:
            try:
                self.__insert_weather(data)
            except sqlite3.IntegrityError:
                self.__update_weather(data)

    def __insert_weather(self, data):
        sql = f"""
                  INSERT INTO ow_weather 
                  VALUES({data["id"]}, 
                         '{data["name"]}', 
                         '{self.sysdate(data["dt"])}', 
                         {data["main"]["temp"]}, 
                         {data["weather"][0]["id"]})
               """
        self.cursor.execute(sql)
        self.connection.commit()

    def __update_weather(self, data):
        sql = f"""
                  SELECT strftime('%s', weather_date)
                    FROM ow_weather
                   WHERE city_id = {data["id"]}
               """
        self.cursor.execute(sql)
        for row in self.cursor:
            if int(row[0]) >= int(data["dt"]):
                # если данные не обновились ничего не делаем
                return None

        sql = f"""
                UPDATE ow_weather
                   SET city_name = '{data["name"]}', 
                       weather_date = '{self.sysdate(data["dt"])}',
                       temperature = {data["main"]["temp"]},
                       weather_id = {data["weather"][0]["id"]}
                 WHERE city_id = {data["id"]}
               """
        self.cursor.execute(sql)
        self.connection.commit()

    def get_weather(self, city_name=None):
        if city_name:
            sql = f"""
                      SELECT *
                        FROM ow_weather
                       WHERE city_name = '{city_name}'
                   """
        else:
            sql = f"""
                      SELECT *
                        FROM ow_weather
                       ORDER BY city_name
                   """
        self.cursor.execute(sql)
        return list(self.cursor)
