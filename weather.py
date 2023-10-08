import requests
import json

def get_weather(api_key, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main_info = data["main"]
        weather_info = data["weather"][0]

        temperature_kelvin = main_info["temp"]
        temperature_celsius = temperature_kelvin - 273.15
        pressure = main_info["pressure"]
        humidity = main_info["humidity"]
        description = weather_info["description"]

        return {
            "temperature_celsius": temperature_celsius,
            "pressure": pressure,
            "humidity": humidity,
            "description": description
        }
    else:
        return None

def load_favorites(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_favorites(filename, favorites):
    with open(filename, 'w') as file:
        json.dump(favorites, file)

if __name__ == "__main__":
    api_key = "a8c991141c63fbe2cf9b00fa064b9de2"
    favorites_filename = "favorites.json"

    favorites = load_favorites(favorites_filename)

    while True:
        print("\nOptions:")
        print("1. Check Weather")
        print("2. Add to Favorites")
        print("3. Remove from Favorites")
        print("4. List Favorites")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            city_name = input("Enter city name: ")
            weather_data = get_weather(api_key, city_name)
            if weather_data:
                print(f"Temperature (in Celsius): {weather_data['temperature_celsius']:.2f}°C")
                print(f"Atmospheric Pressure (hPa): {weather_data['pressure']} hPa")
                print(f"Humidity: {weather_data['humidity']}%")
                print(f"Description: {weather_data['description']}")
            else:
                print("City not found or an error occurred.")

        elif choice == "2":
            city_name = input("Enter city name to add to favorites: ")
            favorites.append(city_name)
            save_favorites(favorites_filename, favorites)

        elif choice == "3":
            city_name = input("Enter city name to remove from favorites: ")
            if city_name in favorites:
                favorites.remove(city_name)
                save_favorites(favorites_filename, favorites)
                print(f"{city_name} removed from favorites.")
            else:
                print(f"{city_name} is not in your favorites.")

        elif choice == "4":
            print("Favorite Cities:")
            for i, city in enumerate(favorites, 1):
                print(f"{i}. {city}")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")
