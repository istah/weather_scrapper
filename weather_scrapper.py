##################
#   Weather scrapper made for some future research purposes
#   Made by Issatay Massalin
#   GitHub link: https://github.com/istah
#   Personal web: https://massalin.me
#   In order to run the code request API key either from these email addresses:
#   issatay.massalin@rompetrol.com
#   issatay@massalin.me
##################



import csv
import pyowm
from datetime import datetime
import time

# Access to API key that is stored in the same directory under 'api_key_weather.txt'
with open('api_key_weather.txt', 'r') as key_file:
    api_key = key_file.read().strip()


locations = [
    {'name': 'Petromidia', 'latitude': 44.34414561686425, 'longitude': 28.64312995919597},
    {'name': 'Vega', 'latitude': 44.962728266313775, 'longitude': 26.024090136370152},
    {'name': 'HeadQuarters', 'latitude': 44.47827607390806, 'longitude': 26.071297673298613},
    # add more locations as needed
]

owm = pyowm.OWM(api_key)

# File name to store the data
filename = 'weather_data.csv'

# Field names for the CSV header
fieldnames = ['Date', 'Location', 'Temperature (°C)', 'Status', 'Humidity']

# Calculate the initial delay until the next 3-hour interval
current_hour = datetime.now().hour
delay_hours = 3 - (current_hour % 3)
initial_delay = delay_hours * 3600  # Convert hours to seconds

time.sleep(initial_delay)

while True:
    # Perform the requests for all locations

    print('Launching the scrapping sequence.')


    for location in locations:
        name = location['name']
        latitude = location['latitude']
        longitude = location['longitude']

        observation = owm.weather_manager().weather_at_coords(latitude, longitude)
        weather = observation.weather

        temperature = weather.temperature('celsius')['temp']
        humidity = weather.humidity
        status = weather.status

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write the data to the CSV file
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()  # Write the header only if the file is empty
            writer.writerow({'Date': current_time, 'Location': name, 'Temperature (°C)': temperature, 'Status': status, 'Humidity': humidity})

        print('Done scrapping for current hours going to sleep for some time and then get data once again.')

        # print(f'Location: {name}')
        # print(f'Temperature: {temperature}°C')
        # print(f'Humidity: {humidity}%')
        # print(f'Status: {status}')
        # print('---------------------')

    # Wait for the next 3-hour interval
    time.sleep(3 * 3600)
