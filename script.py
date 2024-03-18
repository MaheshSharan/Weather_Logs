import logging
import logging.handlers
import os

import requests

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

# Fetch the API key from the environment variable
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
SOME_SECRET = os.getenv('SOME_SECRET')

# Ensure the API key is available
if API_KEY is None:
    logger.error("API key not found. Make sure it's set as an environment variable.")
    raise ValueError("API key not found. Make sure it's set as an environment variable.")
if SOME_SECRET is None:
    logger.error("GitHub token not found. Make sure it's set as an environment variable.")
    raise ValueError("GitHub token not found. Make sure it's set as an environment variable.")

# API endpoint for weather data
API_URL = f'https://api.openweathermap.org/data/2.5/weather?q=Haridwar&appid={API_KEY}&units=metric'
GITHUB_REPO_URL = 'https://api.github.com/repos/MaheshSharan/Weather_Logs/status.log'

def upload_log_to_github(file_path, github_token, repo_url):
    with open(file_path, 'rb') as file:
        content = file.read()
    headers = {
        'Authorization': f'token {github_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'message': 'Update status.log',
        'content': content,
    }
    response = requests.put(repo_url, headers=headers, json=data)
    if response.status_code == 200:
        logger.info('status.log uploaded to GitHub successfully')
    else:
        logger.error(f'Failed to upload status.log to GitHub: {response.status_code} - {response.reason}')

if __name__ == "__main__":
    logger.info(f"API Key: {API_KEY}")

    # Fetch weather data from the API
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        logger.info(f'Weather in Haridwar: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%')

        # Write the log entry to the status.log file
        log_entry = f'Weather in Haridwar: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%'
        with open('status.log', 'a') as file:
            file.write(log_entry + '\n')

        # Upload status.log to GitHub
        upload_log_to_github('status.log', GITHUB_TOKEN, GITHUB_REPO_URL)
    else:
        logger.error(f"Failed to fetch weather data: {response.status_code} - {response.reason}")
