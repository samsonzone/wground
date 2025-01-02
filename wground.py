#!/usr/bin/python3

import requests
from colorama import Fore, Style, init
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Initialize Colorama
init(autoreset=True)

# Constants
API_KEY = "{API KEY}"
STATION_ID = "{STATION ID}"
BASE_URL = f"https://api.weather.com/v2/pws/observations/current?stationId={STATION_ID}&format=json&units=e&apiKey={API_KEY}"

# Suppress warnings
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Convert degrees to compass direction
def degrees_to_compass(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return directions[int((degrees / 22.5) + 0.5) % 16]

# Apply colors to values
def apply_color(value, thresholds, colors, unit=""):
    try:
        value = float(value)
        for limit, color in zip(thresholds, colors):
            if value <= limit:
                return color + f"{value}{unit}" + Style.RESET_ALL
        return Fore.RED + f"{value}{unit}" + Style.RESET_ALL
    except ValueError:
        return f"{value}{unit}"

# Temperature colors
def color_temperature(temp):
    return apply_color(temp, [32, 50, 70, 85], 
                       [Fore.CYAN, Fore.LIGHTBLUE_EX, Fore.YELLOW, Fore.MAGENTA], "°")

# Wind speed colors
def color_wind(speed):
    return apply_color(speed, [0, 5, 15, 25], 
                       [Fore.WHITE, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA], " mph")

# Calculate "Feels Like" Temperature
def calculate_feels_like(temp, wind_speed, humidity):
    try:
        temp, wind_speed, humidity = map(float, [temp, wind_speed, humidity])

        # Wind Chill (<= 50°F and wind >= 3 mph)
        if temp <= 50 and wind_speed >= 3:
            feels_like = 35.74 + 0.6215 * temp - 35.75 * (wind_speed ** 0.16) + 0.4275 * temp * (wind_speed ** 0.16)
            return color_temperature(round(feels_like, 1))

        # Heat Index (>= 80°F and humidity >= 40%)
        elif temp >= 80 and humidity >= 40:
            feels_like = (-42.379 + 2.04901523 * temp + 10.14333127 * humidity
                          - 0.22475541 * temp * humidity - 0.00683783 * temp ** 2
                          - 0.05481717 * humidity ** 2 + 0.00122874 * temp ** 2 * humidity
                          + 0.00085282 * temp * humidity ** 2 - 0.00000199 * temp ** 2 * humidity ** 2)
            return color_temperature(round(feels_like, 1))

    except ValueError:
        return "N/A"

    return "N/A"

# Fetch and display weather data
def get_weather():
    try:
        # Fetch data
        response = requests.get(BASE_URL)
        response.raise_for_status()
        obs = response.json()['observations'][0]

        # Extract Weather Metrics
        temp = obs['imperial'].get('temp', 'N/A')
        dewpt = obs['imperial'].get('dewpt', 'N/A')
        humidity = obs.get('humidity', 'N/A')
        wind_speed = obs['imperial'].get('windSpeed', 'N/A')
        wind_gust = obs['imperial'].get('windGust', 'N/A')
        high_gust = obs['imperial'].get('windGustDailyMax', wind_gust)
        pressure = obs['imperial'].get('pressure', 'N/A')
        precip_rate = obs['imperial'].get('precipRate', 'N/A')
        precip_total = obs['imperial'].get('precipTotal', 'N/A')

        # Wind Direction
        wind_dir = obs.get('winddir', 'N/A')
        wind_dir_compass = degrees_to_compass(wind_dir) if isinstance(wind_dir, (int, float)) else "N/A"

        # Colors
        temp_colored = color_temperature(temp)
        dewpt_colored = color_temperature(dewpt)
        wind_speed_colored = color_wind(wind_speed)
        wind_gust_colored = color_wind(wind_gust)
        high_gust_colored = color_wind(high_gust)

        # Feels Like Calculation
        feels_like = calculate_feels_like(temp, wind_speed, humidity)

        # Output Weather Data
        print(Style.BRIGHT + Fore.RED + "\nWEATHER STATION OBSERVATION" + Style.RESET_ALL)
        print("---------------------------")
        print(f"Observation Time:  {obs.get('obsTimeLocal', 'N/A')}")
        print(f"Location:          {obs.get('neighborhood', 'N/A')}, {obs.get('country', 'N/A')} ({obs.get('stationID', 'N/A')})")
        print(f"Hardware:          {obs.get('softwareType', 'N/A')}\n")

        print(f"Temperature:       {temp_colored}")
        if feels_like:  # Only show "Feels like" if applicable
            print(f"Feels like:        {feels_like}")
        print(f"Dew Point:         {dewpt_colored}")
        print(f"Humidity:          {humidity}%")
        print(f"Wind:              {wind_dir_compass} @ {wind_speed_colored} (Gusts @ {wind_gust_colored})")
        print(f"Max Gust:          {high_gust_colored}")
        print(f"Pressure:          {pressure} inHg")
        print(f"Precip Rate:       {precip_rate} in/hr")
        print(f"Precip Total:      {precip_total} in\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Error parsing weather data: Missing key {e}")

if __name__ == "__main__":
    get_weather()
