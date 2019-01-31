#

APP_ID_FILENAME = "app.id"


class OpenWeatherAppId:
    def __init__(self):
        self.__APP_ID = self.load_appid(APP_ID_FILENAME)

    @staticmethod
    def load_appid(filename):
        try:
            f = open(filename, "r", encoding="UTF-8")
            app_id = f.readlines()[0]
        except FileNotFoundError as e:
            raise Exception(f"ABORTED! File '{APP_ID_FILENAME}' not found")
        return app_id

    def get_app_id(self):
        return self.__APP_ID

