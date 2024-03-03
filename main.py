import datetime as dt
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

app = Flask(__name__)

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
    url = "https://api.spotify.com/v1/browse/search"
    headers = get_auth_header(token)
    query = f"?q={categories}&type=playlist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    #print(json_result)
    return json_result


token = get_token()

weather_spotify_dict = {
    "thunderstorm": ["intense", "dramatic", "stormy"],
    "thunderstorm with light rain": ["lightning", "showers", "electric"],
    "thunderstorm with rain": ["rainy", "thunder", "storm"],
    "thunderstorm with heavy rain": ["heavy rain", "thunder", "stormy"],
    "light thunderstorm": ["gentle", "rumbling", "light storm"],
    "thunderstorm": ["thunder", "storm", "lightning"],
    "heavy thunderstorm": ["heavy", "thunder", "storm"],
    "ragged thunderstorm": ["ragged", "thunder", "stormy"],
    "thunderstorm with light drizzle": ["light drizzle", "thunder", "storm"],
    "thunderstorm with drizzle": ["drizzle", "thunder", "storm"],
    "thunderstorm with heavy drizzle": ["heavy drizzle", "thunder", "storm"],
    "drizzle": ["light rain", "gentle", "misty"],
    "light intensity drizzle": ["light drizzle", "gentle", "misty"],
    "drizzle": ["drizzle", "gentle rain", "misty"],
    "heavy intensity drizzle": ["heavy drizzle", "heavy rain", "wet"],
    "light intensity drizzle rain": ["light drizzle rain", "gentle rain", "misty"],
    "drizzle rain": ["drizzle rain", "rainy", "wet"],
    "heavy intensity drizzle rain": ["heavy drizzle rain", "heavy rain", "wet"],
    "shower rain and drizzle": ["shower rain", "drizzle", "rainy"],
    "heavy shower rain and drizzle": ["heavy shower rain", "heavy drizzle", "stormy"],
    "shower drizzle": ["shower drizzle", "rainy", "misty"],
    "rain": ["rainy", "soothing", "wet"],
    "light rain": ["light rain", "gentle", "calm"],
    "moderate rain": ["moderate rain", "steady", "wet"],
    "heavy intensity rain": ["heavy rain", "intense", "pouring"],
    "very heavy rain": ["very heavy rain", "torrential", "stormy"],
    "extreme rain": ["extreme rain", "intense", "stormy"],
    "freezing rain": ["freezing rain", "icy", "cold"],
    "light intensity shower rain": ["light shower rain", "gentle rain", "calm"],
    "shower rain": ["shower rain", "rainy", "wet"],
    "heavy intensity shower rain": ["heavy shower rain", "intense rain", "stormy"],
    "ragged shower rain": ["ragged shower rain", "stormy", "wet"],
    "snow": ["winter", "snowy", "chill"],
    "light snow": ["light snow", "gentle", "winter"],
    "snow": ["snow", "winter wonderland", "cold"],
    "heavy snow": ["heavy snow", "winter", "stormy"],
    "sleet": ["sleet", "icy", "cold"],
    "light shower sleet": ["light shower sleet", "icy", "cold"],
    "shower sleet": ["shower sleet", "icy", "cold"],
    "light rain and snow": ["light rain and snow", "winter", "wet"],
    "rain and snow": ["rain and snow", "winter", "wet"],
    "light shower snow": ["light shower snow", "gentle snow", "calm"],
    "shower snow": ["shower snow", "snowy", "winter"],
    "heavy shower snow": ["heavy shower snow", "heavy snow", "stormy"],
    "atmosphere": ["atmospheric", "mystical", "ambient"],
    "mist": ["mystical", "serene", "misty"],
    "smoke": ["atmospheric", "ambient", "smoky"],
    "haze": ["dreamy", "calm", "hazy"],
    "dust": ["desert", "dry", "dusty"],
    "sand/dust whirls": ["sand/dust whirls", "windy", "desert"],
    "fog": ["mysterious", "ethereal", "foggy"],
    "sand": ["warm", "beachy", "sandy"],
    "dust": ["dusty", "dry", "arid"],
    "volcanic ash": ["volcanic ash", "gray", "hazy"],
    "squalls": ["windy", "turbulent", "squally"],
    "tornado": ["tornado", "whirlwind", "chaotic"],
    "clear sky (day)": ["clear", "bright", "sunny"],
    "clear sky (night)": ["clear", "starry", "tranquil"],
    "few clouds (day)": ["partly cloudy", "scattered", "sunny spells"],
    "few clouds (night)": ["starry", "clear", "calm"],
    "scattered clouds (day)": ["partly cloudy", "sunny", "scattered"],
    "scattered clouds (night)": ["starry", "cloudy", "calm"],
    "broken clouds (day)": ["cloudy", "overcast", "gloomy"],
    "broken clouds (night)": ["cloudy", "overcast", "calm"],
    "overcast clouds (day)": ["cloudy", "overcast", "gloomy"],
    "overcast clouds (night)": ["cloudy", "overcast", "calm"]
}


@app.route("/get-weather/<city>")
def get_weather(city):
    url = WEATHER_BASE_URL + "appid=" + WEATHER_API_KEY + "&q=" + city
    response = requests.get(url).json()
    description = response["weather"][0]["description"]
    search_items = weather_spotify_dict.get(description, [])
    playlist = search_for_playlist(token, "hello")
    #return jsonify(description), 200
    return jsonify({"description": description, "serach_items": search_items, "playlists": playlist})


if __name__ == "__main__":
    app.run(debug=True)