import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def log(message):
    print(f"{datetime.now()}: {message}")
    sys.stdout.flush()


def descriptions_mapping(weather_code):
    """Collect the descriptions and image based on weather code."""
    with open("descriptions.json", "r") as f:
        weather_descriptions = json.load(f)

    # Select the correct descriptions using weather_code -- Note always for "day".
    weather_info = weather_descriptions.get(str(weather_code), {}).get("day", {})

    # Return dictionary with description and image.
    return {
        "description": weather_info.get("description", "Unknown"),
        "image": weather_info.get("image", "Unknown"),
    }


def get_forecast(db_password=os.environ.get("WEATHER_DB_PASSWORD")):
    """Collect data from SQL table for inputting into email"""
    today_sql =     """SELECT * FROM weather_forecast
                    WHERE forecast_date = CURDATE();"""
    tomorrow_sql =  """SELECT * FROM weather_forecast
                    WHERE forecast_date = CURDATE()+interval 1 day;"""

    try:
        # Connect to database.
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=db_password,
            database="weather_project"
        )
        cursor = db.cursor(dictionary=True)

        # Grab today's data.
        log("Attempting to get forecast.")
        cursor.execute(today_sql)
        today_forecast = cursor.fetchone()

        # Grab tomorrow's data
        cursor.execute(tomorrow_sql)
        tomorrow_forecast = cursor.fetchone()

        # Close database connection and return data.
        log("Forecast data collected.")
        cursor.close()
        db.close()
        return today_forecast, tomorrow_forecast

    # Catch errors with database connection.
    except mysql.connector.Error as err:
        log(f"Database connection error: {err}")
        sys.exit(1)


def format_email(db_password=os.environ.get("WEATHER_DB_PASSWORD")):
    """Adds data and formats the email."""
    try:
        today_forecast, tomorrow_forecast = get_forecast(db_password)
        today_description = descriptions_mapping(today_forecast["weather_code"])
        tomorrow_description = descriptions_mapping(tomorrow_forecast["weather_code"])

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width">
            <title>Weather Forecast</title>
        </head>
        <body style="font-family: Ubuntu, 'Roboto Medium', Calibri; font-size: 18px; line-height: 1.6; color: #ffffff; background-color: #121212; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #f5cc30; text-align: center;">Weather Forecast for {today_forecast["city"]}</h1>
        
            <div style="background-color: #1e1e1e; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #4ec953;">Today ({today_forecast["forecast_date"]})</h2>
                <img src="{today_description["image"]}" alt="Weather Icon" style="display: block; margin: 10px 0; width: 100px; height: auto;">
                <p><strong>Temperature:</strong> {today_forecast["temp_min"]}&deg;C to {today_forecast["temp_max"]}&deg;C</p>
                <p><strong>Weather:</strong> {today_description["description"]}</p>
                <p><strong>Precipitation:</strong> {today_forecast["precipitation_sum"]}mm - ({today_forecast["precipitation_probability"]}% chance)</p>
            </div>
        
            <div style="background-color: #1e1e1e; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #21b4f3;">Tomorrow ({tomorrow_forecast["forecast_date"]})</h2>
                <img src="{tomorrow_description["image"]}" alt="Weather Icon" style="display: block; margin: 10px 0; width: 100px; height: auto;">
                <p><strong>Temperature:</strong> {tomorrow_forecast["temp_min"]}&deg;C to {tomorrow_forecast["temp_max"]}&deg;C</p>
                <p><strong>Weather:</strong> {tomorrow_description["description"]}</p>
                <p><strong>Precipitation:</strong> {tomorrow_forecast["precipitation_sum"]}mm - ({tomorrow_forecast["precipitation_probability"]}% chance)</p>
            </div>
        </body>
        </html>
        """
        return html_content

    except Exception as e:
        print(f"Error while formatting the email: {e}")


def email_send():
    # Initialise sending email account
    host = "smtp-mail.outlook.com"
    port = 587

    from_addr = "weatheralert098@outlook.com"
    to_addr = "wemyssstephen@gmail.com"
    password = os.environ.get("WEATHER_EMAIL_PASSWORD")


    # Create email
    message = MIMEMultipart("alternative")
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = "Today's Weather Forecast"

    # Create body
    html = format_email()
    part = MIMEText(html, "html")
    message.attach(part)

    # Send the email
    try:
        log(f"Connection to {host}: {port}")
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            log("Connection established.")
            log("TLS starting...")
            server.starttls()
            server.ehlo()
            log("Logging in...")
            server.login(from_addr, password)
            log("Login successful.")
            log("Sending email...")
            server.sendmail(from_addr, to_addr, message.as_string())
            log("Email sent!")
    except smtplib.SMTPException as e:
        log(f"SMTP exception: {e}")
    except Exception as e:
        log(f"Error while sending email: {e}")





