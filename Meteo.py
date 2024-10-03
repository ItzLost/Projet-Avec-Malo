import requests
from datetime import datetime, timedelta

def degree_to_direction(degree):
    if degree is None:
        return "Inconnu"
    if degree >= 337.5 or degree < 22.5:
        return "Nord"
    elif 22.5 <= degree < 67.5:
        return "Nord-Est"
    elif 67.5 <= degree < 112.5:
        return "Est"
    elif 112.5 <= degree < 157.5:
        return "Sud-Est"
    elif 157.5 <= degree < 202.5:
        return "Sud"
    elif 202.5 <= degree < 247.5:
        return "Sud-Ouest"
    elif 247.5 <= degree < 292.5:
        return "Ouest"
    elif 292.5 <= degree < 337.5:
        return "Nord-Ouest"

def get_weather_forecast(api_key, city, date_str, horaires_disponibles):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        'key': api_key,
        'q': city,
        'days': 1,  # Limiter à 1 jour
        'aqi': 'no',
        'alerts': 'no'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        city_name = data['location']['name']
        print(f"Prévisions météo pour {city_name} le {date_str} :")
        
        for hour in data['forecast']['forecastday'][0]['hour']:
            hour_time = datetime.strptime(hour['time'], "%Y-%m-%d %H:%M")
            hour_str = hour_time.strftime("%H:%M")  # Format HH:MM

            if hour_str in horaires_disponibles:
                print(f"\nDate : {hour_time.strftime('%Y-%m-%d %H:%M')}")
                print(f"Température : {hour['temp_c']}°C")
                print(f"Conditions : {hour['condition']['text']}")
                print(f"Vitesse du vent : {round(hour['wind_kph'] / 1.852, 1)} noeuds")
                print(f"Direction du vent : {degree_to_direction(hour['wind_degree'])}")

    else:
        print("Erreur lors de la récupération des données :", response.status_code)

def demander_horaires():
    horaires = input("Entrez vos horaires disponibles (ex: 09:00-12:00, 14:00-18:00) : ")
    horaires_disponibles = []
    try:
        for plage in horaires.split(","):
            start_time, end_time = plage.strip().split("-")
            start_datetime = datetime.strptime(start_time.strip(), "%H:%M")
            end_datetime = datetime.strptime(end_time.strip(), "%H:%M")
            current_time = start_datetime
            
            while current_time <= end_datetime:
                horaires_disponibles.append(current_time.strftime("%H:%M"))  # Format HH:MM
                current_time += timedelta(hours=1)  # Ajoute chaque heure
    except ValueError:
        print("Erreur de format dans les horaires.")
    
    return horaires_disponibles

if __name__ == "__main__":
    api_key = "6c49665ad5b343f99b7121258240110"  # Remplacez par votre clé API
    city = input("Entrez le nom de la ville : ")
    date_str = input("Entrez la date (format AAAA-MM-JJ) : ")

    horaires_disponibles = demander_horaires()
    print("Horaires disponibles :", horaires_disponibles)
    
    get_weather_forecast(api_key, city, date_str, horaires_disponibles)


