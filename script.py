import requests
import datetime
import os


# Fetch the API key from the environment variable
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Ensure the API key is available
if API_KEY is None:
    raise ValueError("API key not found. Make sure it's set as a GitHub secret.")
# API endpoint for weather data
API_URL = f'https://api.openweathermap.org/data/2.5/weather?q=Haridwar&appid={API_KEY}&units=metric'

# Fetch weather data from the API
response = requests.get(API_URL)
data = response.json()

# Extract relevant information from the response
weather_description = data['weather'][0]['description']
temperature = data['main']['temp']
humidity = data['main']['humidity']

# Create a timestamp for the log entry
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Format the log entry
log_entry = f'{timestamp} - Weather: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%'

# Print the weather information
print(log_entry)

# Write the log entry to the status.log file
with open('status.log', 'a') as file:
    file.write(log_entry + '\n')
