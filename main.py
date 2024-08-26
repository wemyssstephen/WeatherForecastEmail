import os
import sys
import requests

import mysql.connector
from datetime import datetime


def log(message):
    print(f"{datetime.now()}: {message}")
    sys.stdout.flush()

def main():
    log("Script started.")

    db_password = os.environ.get("WEATHER_DB_PASSWORD")

    if not db_password:
        log("Error: Environment variables not set properly.")
        sys.exit(1)

    try:
        # Database connection
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=db_password,
            database="weather_project"
        )
        cursor = db.cursor()
        log("Database connected successfully.")
    except mysql.connector.Error as err:
        log(f"Database connection error: {err}")
        sys.exit(1)

    # API request
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 53.9576,  # Latitude for York, UK
        "longitude": -1.0827,  # Longitude for York, UK
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum",
                  "precipitation_hours", "precipitation_probability_mean"], "timezone":"Europe/London"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        log("Weather data received successfully.")

        # Insert data into database
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """INSERT INTO weather_forecast
                 (city, updated_at, forecast_date, weather_code, temp_max, temp_min, 
                  sunrise, sunset, precipitation_sum, precipitation_hours, precipitation_probability)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE
                 city = VALUES(city),
                 updated_at = VALUES(updated_at),
                 weather_code = VALUES(weather_code),
                 temp_max = VALUES(temp_max),
                 temp_min = VALUES(temp_min),
                 sunrise = VALUES(sunrise),
                 sunset = VALUES(sunset),
                 precipitation_sum = VALUES(precipitation_sum),
                 precipitation_hours = VALUES(precipitation_hours),
                 precipitation_probability = VALUES(precipitation_probability)"""

        daily = weather_data['daily']
        for i in range(len(daily['time'])):
            values = (
                "York,GB",
                current_time,
                datetime.fromisoformat(daily['time'][i]).date(),
                str(daily['weather_code'][i]),
                float(daily['temperature_2m_max'][i]),
                float(daily['temperature_2m_min'][i]),
                daily['sunrise'][i],
                daily['sunset'][i],
                float(daily['precipitation_sum'][i]),
                float(daily['precipitation_hours'][i]),
                float(daily['precipitation_probability_mean'][i]),
            )

            try:
                cursor.execute(sql, values)
                db.commit()
                print(f"Data inserted correctly for {values[2]}")
            except mysql.connector.Error as err:
                print(f"Data received, but MySQL error prevented inserting data for {values[2]}")
                print(f"The error received was: {err}")
                db.rollback()

    except Exception as err:
        log(f"Error fetching or processing the weather data: {err}")
        log(f"Weather data structure: {weather_data}")

    # Close database connection
    cursor.close()
    db.close()
    log("Script finished.")

if __name__ == "__main__":
    main()








