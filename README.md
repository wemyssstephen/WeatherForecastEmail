# Weather Forecast Email Application

A Python application that fetches weather forecast data for York, UK, stores it in a MySQL database, and sends email updates. Built as a learning project to practice working with APIs, databases, and email functionality.

## Features

- Fetches daily weather forecast data from Open-Meteo API
- Stores forecast information in a MySQL database
- Sends email updates with weather information
- Handles data updates and duplicates
- Includes error logging and exception handling

## Technical Details

### Technologies Used
- Python
- MySQL
- External APIs:
  - Open-Meteo Weather API
- Libraries:
  - `requests` for API calls
  - `mysql-connector-python` for database operations

### Data Points Collected
- Weather code
- Maximum and minimum temperatures
- Sunrise and sunset times
- Precipitation data (sum, hours, probability)

## Project Status

This is a learning project I built while teaching myself Python. While functional, there are several improvements I'd like to make:

- Add configuration file for easy location changes
- Implement unit tests
- Add a web interface
- Expand email formatting options

Building this project helped me understand:
- Working with REST APIs and JSON data
- Database operations and SQL query optimization
- Environment variables for secure credential management
- Error handling and logging best practices
