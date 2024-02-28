import datetime as dt
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/get-weather/<city>")
def get_weather(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    description = response["weather"][0]["description"]
    return jsonify(description), 200


if __name__ == "__main__":
    app.run(debug=True)