import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 53.9576,
    "longitude": -1.0827,
    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum",
              "precipitation_hours", "precipitation_probability_mean"],
    "timezone": "Europe/London"
}

response = requests.get(url, params=params)
data = response.json()

print(data)