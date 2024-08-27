import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main import get_forecast, descriptions_mapping, log


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
            <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'JetBrains Mono', monospace;
                    line-height: 1.6;
                    color: #ffffff;
                    background-color: #121212;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #ffffff}}
            .forecast-box {{
                background-color: #1e1e1e;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .today-heading {{
                color: #4caf50;
            }}
            .tomorrow-heading {{
                color: #2196f3;
            }}
            .weather-icon {{
                display: block;
                margin: 10px 0
                width: 100px
                height: auto;
            }}
            </style>
        </head>
        <body>
            <h1>Weather Forecast for {today_forecast["city"]}</h1>
    
            <div class="forecast-box">
                <h2 class="today-heading">Today ({today_forecast["forecast_date"]})</h2>
                <img src="{today_description["image"]}" alt="Weather Icon" class="weather-icon">
                <p><strong>Temperature:</strong>{today_forecast["temp_min"]}&deg;C to {today_forecast["temp_max"]}&deg;C</p>
                <p><strong>Weather:</strong> {today_description["description"]}</p>
    
                <p><strong>Precipitation:</strong>{today_forecast["precipitation_sum"]}mm - ({today_forecast["precipitation_probability"]}% chance)</p>
            </div>
    
            <div class="forecast-box">
                <h2 style="color: #1e88e5;">Tomorrow ({tomorrow_forecast["forecast_date"]})</h2>
                <img src="{tomorrow_description["image"]}" alt="Weather Icon" class="weather-icon">
                <p><strong>Temperature:</strong> {tomorrow_forecast["temp_min"]}&deg;C to
                {tomorrow_forecast["temp_max"]}&deg;C</p>
                <p><strong>Weather:</strong> {tomorrow_description["description"]}</p>
    
                <p><strong>Precipitation:</strong>{tomorrow_forecast["precipitation_sum"]}mm - ({tomorrow_forecast["precipitation_probability"]}% chance)</p>
            </div>
        </body>
        </html>
        """
        return html_content

    except Exception as e:
        print(f"Error while formatting the email: {e}")


def email_send(message):
    # Initialise sending email account
    host = "smtp.gmail.com"
    port = 587

    from_addr = "weatheralert089@gmail.com"
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
        smtp = smtplib.SMTP(host, port)
        status_code, response = smtp.ehlo()
        log(f"Contacting the server: {status_code}, {response}")

        status_code, response = smtp.starttls()
        log(f"Starting TLS connection: {status_code}, {response}")

        status_code, response = smtp.login(from_addr, password)
        log(f"Login successful: {status_code}, {response}")

        smtp.sendmail(from_addr, to_addr, message)
        smtp.quit()
    except Exception as e:
        log(f"Error while sending email: {e}")

if __name__ == '__main__':
    email_send()





