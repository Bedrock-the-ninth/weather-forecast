import os
import requests
from dotenv import load_dotenv

load_dotenv(".env")


class OWMDataGrab:
    def __init__(self):

        self.my_lat = os.getenv(MY_LAT)
        self.my_lng = os.getenv(MY_LONG)
        self.api_key = os.getenv(API_KEY)
        self.OWM_Endpoint = os.getenv(OWM_ENDPOINT)

        self.weather_params = {
            "lat": self.my_lat,
            "lon": self.my_lng,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 5
        }

        self.weather_data = None

        self.connection_init()

    def connection_init(self):
        response = requests.get(url=self.OWM_Endpoint, params=self.weather_params)
        response.raise_for_status()
        self.weather_data = response.json()['list']

    def weather_check(self):

        temp_mean = round(sum([interval['main']['temp'] for interval in self.weather_data]) / 5, 2)
        feels_like_mean = round(sum([interval['main']['feels_like'] for interval in self.weather_data]) / 5, 2)

        condition_codes = [
            {interval['dt_txt'][11:16]: interval['weather'][0]['id']}
            for interval in self.weather_data
            if interval['weather'][0]['id'] < 700
        ]

        if len(condition_codes) < 1:
            weather_condition = "clear"
        else:
            weather_condition = [list(i.keys())[0] for i in condition_codes]

        return [temp_mean, feels_like_mean, weather_condition]

    def forcast_analysis(self):
        [temp_mean, feels_like_mean, weather_condition] = self.weather_check()

        match weather_condition:
            case "clear":
                weather_condition = ("Weather will most likely be clear in the upcomming 15 hours. "
                                     "No need for an umbrella!")
            case _:
                weather_condition = ("There is a possibility of turmoil in the climate at these hours:"
                                     f"\n{', '.join(weather_condition)}"
                                     "\nCarrying an umbrella would be a wise choice!")

        message = (f"Average temperature in the upcomming 15 hours is {temp_mean}.\n"
                   f"However, it may feel like {feels_like_mean}\n{weather_condition}")

        return message
