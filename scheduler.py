from dotenv import load_dotenv
load_dotenv()

import main, os

def run_job():
    """Schedules app to run at 00:30 if computer is on."""
    main.log("Running weather app...")
    try:
        main.run_weather_app()
    except Exception as e:
        main.log(f"Error occurred: {str({e})}")

if __name__ == '__main__':
    run_job()
