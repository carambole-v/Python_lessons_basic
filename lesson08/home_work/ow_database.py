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
        try:
            self.__create_tables()
        except:
            pass

    def __del__(self):
        self.connection.close()

    def __create_tables(self):
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
        return datetime.fromtimestamp(timestamp)

    def add_weather(self, data):
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
                  SELECT strftime('%s', weather_date) - 3600*3
                    FROM ow_weather
                   WHERE city_id = {data["id"]}
               """
        self.cursor.execute(sql)
        for row in self.cursor:
            print(int(row[0]), int(data["dt"]))
            if int(row[0]) >= int(data["dt"]):
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
