import requests
from datetime import datetime

def getWeatherForecast(apiKey, city, dateStr, availableHours, lang):
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
        print(lang == 'en' and f'Weather forecast for {cityName} on {dateStr}:' or f'Prévisions météo pour {cityName} le {dateStr}')

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
            print(lang == 'en' and f'You can go wingfoiling from {wingfoilingHours[0]}h to {wingfoilingHours[-1]}h.' or f'Vous pouvez faire du wingfoil de {wingfoilingHours[0]}h à {wingfoilingHours[-1]}h.')
        elif len(nonWingfoilingHours) <= 0 and len(availableHours) > 1:
            print(lang == 'en' and 'You can\'t go wingfoiling in the specified range.' or f'Vous ne pouvez pas faire de wingfoil dans la plage horraire spécifiée.')

        if len(nonWingfoilingHours) > 1:
            print(lang == 'en' and f'You can\'t surf between: {"h, ".join(nonWingfoilingHours)}h.' or f'Vous ne pouvez pas surfer entre : {"h, ".join(nonWingfoilingHours)}h.')
        elif len(nonWingfoilingHours) == 1:
            print(lang == 'en' and f'You can\'t surf at: {"h, ".join(nonWingfoilingHours)}h.' or f'Vous ne pouvez pas surfer sur : {"h, ".join(nonWingfoilingHours)}h.')

        if countTemp > 0:
            avgTemp = totalTemp / countTemp
            print(lang == 'en' and f'Average air temperature: {avgTemp:.1f}°C.' or f'Température moyenne de l\'air : {avgTemp:.1f}°C.')
            print(lang == 'en' and f'Estimated water temperature: {avgTemp - 2:.1f}°C.' or f'')

        if countWindSpeed > 0:
            avgWindSpeed = totalWindSpeed / countWindSpeed
            print(lang == 'en' and f'Average wind speed: {avgWindSpeed:.1f} knots.' or f'Vitesse moyenne du vent : {avgWindSpeed:.1f} noeuds.')

        if windDirections:
            print(lang == 'en' and f'Wind directions: {"°, ".join(map(str, windDirections))}°.' or f'Directions du vent : {"°, ".join(map(str, windDirections))}°.')

    else:
        print(lang == 'en' and 'Error retrieving data:' or 'Erreur lors de la récupération des données:', response.status_code)

def askAvailableHours(lang):
    hours = input(lang == 'en' and 'Enter your available hours (like 9-12, 14-18) or just hit Enter to use the current hour: ' or f'Entrez vos heures disponibles (comme 9-12, 14-18) ou appuyez simplement sur Entrée pour utiliser l\'heure actuelle :')
    availableHours = []
    
    if not hours.strip():
        now = datetime.now()
        availableHours.append(now.strftime('%H'))
        print(lang == 'en' and f'Using current hour: {now.strftime("%H")}:00' or f'Utilisation de l\'heure actuelle : {now.strftime("%H")}:00')
    else:
        try:
            for rangeStr in hours.split(','):
                startHour, endHour = map(int, rangeStr.strip().split('-'))
                for hour in range(startHour, endHour + 1):
                    availableHours.append(str(hour))
        except ValueError:
            print(lang == 'en' and 'Error in time format.' or f'Erreur dans le format de l\'heure.')
    
    return availableHours

if __name__ == '__main__':
    apiKey = '6c49665ad5b343f99b7121258240110'
    language = input('Language wanted (fr-en): ')

    if 'en' in language.lower():
        language = 'en'
    elif 'fr' in language.lower():
        print('Le langage a été changé en Français.')
        language = 'fr'
    else:
        print('Language is not available or not recognized. Using english.')
        language = 'en'

    city = input(language == 'en' and 'Enter the name of the city: ' or 'Enrtez le nom de la ville: ')
    dateStr = input(language == 'en' and 'Enter the date (YYYY-MM-DD) or just hit Enter for today: ' or 'Entrez la date (AAAA-MM-JJ) ou appuyez simplement sur Entrée pour aujourd\'hui : ')

    

    if not dateStr.strip():
        dateStr = datetime.now().strftime('%Y-%m-%d')
        print(language == 'en' and f'Using today\'s date: {dateStr}' or f'Utilisation de la date d\'aujourd\'hui : {dateStr}')
    

    availableHours = askAvailableHours(language)
    print(language == 'en' and 'Available hours:' or 'Horaires disponibles :', availableHours)
    
    getWeatherForecast(apiKey, city, dateStr, availableHours, language)

