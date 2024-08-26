import os
import smtplib

def format_email(forecast):


def email_send():
    host = "smtp.gmail.com"
    port = 587

    from_addr = "weatheralert089@gmail.com"
    to_addr = "wemyssstephen@gmail.com"
    password = os.environ.get("WEATHER_EMAIL_PASSWORD")

    message = """Subject: Weather Alert
    
    Hi Stephen,
    
    This is a test email.
    
    Thanks,
    Stephen"""

    smtp = smtplib.SMTP(host, port)
    status_code, response = smtp.ehlo()
    print(f"Contacting the server: {status_code}, {response}")

    status_code, response = smtp.starttls()
    print(f"Starting TLS connection: {status_code}, {response}")

    status_code, response = smtp.login(from_addr, password)
    print(f"Login successful: {status_code}, {response}")

    smtp.sendmail(from_addr, to_addr, message)
    smtp.quit()

if __name__ == '__main__':
    email_send()





