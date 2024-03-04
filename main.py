from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import base64
import json
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_playlist(token, categories):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={categories}&type=playlist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    if len(json_result) == 0:
        return ("Playlists not found")
    return json_result


token = get_token()

weather_spotify_dict = {
    "thunderstorm": "thunderstorm mix",
    "thunderstorm with light rain": "thunderstorm mix",
    "thunderstorm with rain": "thunderstorm mix",
    "thunderstorm with heavy rain": "thunderstorm mix",
    "light thunderstorm": "thunderstorm mix",
    "thunderstorm": "thunderstorm mix",
    "heavy thunderstorm": "thunderstorm mix",
    "ragged thunderstorm": "thunderstorm mix",
    "thunderstorm with light drizzle": "thunderstorm mix",
    "thunderstorm with drizzle": "thunderstorm mix",
    "thunderstorm with heavy drizzle": "thunderstorm mix",
    "drizzle": "calming drizzle",
    "light intensity drizzle": "serene",
    "drizzle": "soothing",
    "heavy intensity drizzle": "rain",
    "light intensity drizzle rain": "rain",
    "drizzle rain": "calming rain",
    "heavy intensity drizzle rain": "rain drizzle",
    "shower rain and drizzle": "rain shower",
    "heavy shower rain and drizzle": "heavy rain",
    "shower drizzle": "rainy day",
    "rain": "rainy day",
    "light rain": "calming rain",
    "moderate rain": "rainy day",
    "heavy intensity rain": "heavy rain",
    "very heavy rain": "heavy rain",
    "extreme rain": "heavy rain",
    "freezing rain": "cold rain",
    "light intensity shower rain": "light rain",
    "shower rain": "rain shower",
    "heavy intensity shower rain": "heavy rain",
    "ragged shower rain": "rain shower",
    "snow": "snow day",
    "light snow": "snow day",
    "heavy snow": "snowstorm",
    "sleet": "light snow",
    "light shower sleet": "light snow",
    "shower sleet": "light snow",
    "light rain and snow": "cold rain",
    "rain and snow": "cold rain",
    "light shower snow": "snow storm",
    "shower snow": "snow day",
    "heavy shower snow": "snow day",
    "mist": "misty rain",
    "smoke": "smokey",
    "haze": "dreamy",
    "dust": "hazy",
    "sand/dust whirls": "hazy",
    "fog": "mysterious",
    "sand": "sandy",
    "dust": "dusty",
    "volcanic ash": "hazy",
    "squalls": "stormy",
    "tornado": "gusty",
    "clear sky": "sunny day",
    "few clouds": "sunny",
    "scattered clouds": "sunny",
    "broken clouds": "cloudy",
    "overcast clouds": "gloomy"
}


@app.route("/get-weather/<city>")
def get_weather(city):
        try:
            url = WEATHER_BASE_URL + "appid=" + WEATHER_API_KEY + "&q=" + city
            response = requests.get(url).json()
            if "weather" in response:
                description = response["weather"][0]["description"]
                search_items = weather_spotify_dict.get(description, [])
                playlist = search_for_playlist(token, search_items)
                return jsonify({"response": response, "search_items": search_items, "playlists": playlist})
            else:
                return jsonify({"error": response["message"]})
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)