import requests
from datetime import datetime, timedelta

def getWeatherForecast(apiKey, city, dateStr, availableHours):
    baseUrl = 'http://api.weatherapi.com/v1/forecast.json'
    params = {
        'key': apiKey,
        'q': city,
        'days': 1,
        'aqi': 'no',
        'alerts': 'no'
    }

    response = requests.get(baseUrl, params=params)

    if response.status_code == 200:
        data = response.json()
        cityName = data['location']['name']
        print(f'Weather forecast for {cityName} on {dateStr}:')

        wingfoilingHours = []
        nonWingfoilingHours = []
        totalTemp = 0
        totalWindSpeed = 0
        countTemp = 0
        countWindSpeed = 0
        windDirections = []

        for hour in data['forecast']['forecastday'][0]['hour']:
            hourTime = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
            hourStr = hourTime.strftime('%H')

            if hourStr in availableHours:
                windSpeedKnots = round(hour['wind_kph'] / 1.852, 1)
                windDirection = hour['wind_dir']
                temperature = hour['temp_c']

                totalTemp += temperature
                countTemp += 1
                totalWindSpeed += windSpeedKnots
                countWindSpeed += 1
                windDirections.append(windDirection)

                if windSpeedKnots >= 10 and (windDirection in range(180, 361) or windDirection == 0):
                    wingfoilingHours.append(hourStr)
                else:
                    nonWingfoilingHours.append(hourStr)

        if wingfoilingHours:
            print(f'You can go wingfoiling from {wingfoilingHours[0]} to {wingfoilingHours[-1]}.')
        elif len(nonWingfoilingHours) <= 0 and len(availableHours) > 1:
            print('You can\'t go wingfoiling in the specified range.')

        if len(nonWingfoilingHours) > 1:
            print(f'You can\'t surf between: {", ".join(nonWingfoilingHours)}.')
        elif len(nonWingfoilingHours) == 1:
            print(f'You can\'t surf at: {", ".join(nonWingfoilingHours)}.')

        if countTemp > 0:
            avgTemp = totalTemp / countTemp
            print(f'Average air temperature: {avgTemp:.1f}°C.')
            print(f'Estimated water temperature: {avgTemp - 2:.1f}°C.')

        if countWindSpeed > 0:
            avgWindSpeed = totalWindSpeed / countWindSpeed
            print(f'Average wind speed: {avgWindSpeed:.1f} knots.')

        if windDirections:
            print(f'Wind directions: {", ".join(map(str, windDirections))}°.')

    else:
        print('Error retrieving data:', response.status_code)

def askAvailableHours():
    hours = input('Enter your available hours (like 9-12, 14-18) or just hit Enter to use the current hour: ')
    availableHours = []
    
    if not hours.strip():
        now = datetime.now()
        availableHours.append(now.strftime('%H'))
        print(f'Using current hour: {now.strftime("%H")}:00')
    else:
        try:
            for rangeStr in hours.split(','):
                startHour, endHour = map(int, rangeStr.strip().split('-'))
                for hour in range(startHour, endHour + 1):
                    availableHours.append(str(hour))
        except ValueError:
            print('Error in time format.')
    
    return availableHours

if __name__ == '__main__':
    apiKey = '6c49665ad5b343f99b7121258240110'
    city = input('Enter the name of the city: ')
    dateStr = input('Enter the date (YYYY-MM-DD) or just hit Enter for today: ')

    if not dateStr.strip():
        dateStr = datetime.now().strftime('%Y-%m-%d')
        print(f'Using today\'s date: {dateStr}')

    availableHours = askAvailableHours()
    print('Available hours:', availableHours)
    
    getWeatherForecast(apiKey, city, dateStr, availableHours)

