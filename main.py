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
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")

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
    json_result = json.loads(result.content)
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

country_two_letter_code = {
    'Afghanistan': 'AF',
    'Albania': 'AL',
    'Algeria': 'DZ',
    'Andorra': 'AD',
    'Angola': 'AO',
    'Antigua and Barbuda': 'AG',
    'Argentina': 'AR',
    'Armenia': 'AM',
    'Australia': 'AU',
    'Austria': 'AT',
    'Azerbaijan': 'AZ',
    'Bahamas': 'BS',
    'Bahrain': 'BH',
    'Bangladesh': 'BD',
    'Barbados': 'BB',
    'Belarus': 'BY',
    'Belgium': 'BE',
    'Belize': 'BZ',
    'Benin': 'BJ',
    'Bhutan': 'BT',
    'Bolivia': 'BO',
    'Bosnia and Herzegovina': 'BA',
    'Botswana': 'BW',
    'Brazil': 'BR',
    'Brunei Darussalam': 'BN',
    'Bulgaria': 'BG',
    'Burkina Faso': 'BF',
    'Burundi': 'BI',
    'Cabo Verde': 'CV',
    'Cambodia': 'KH',
    'Cameroon': 'CM',
    'Canada': 'CA',
    'Central African Republic': 'CF',
    'Chad': 'TD',
    'Chile': 'CL',
    'China': 'CN',
    'Colombia': 'CO',
    'Comoros': 'KM',
    'Congo': 'CG',
    'Costa Rica': 'CR',
    'Croatia': 'HR',
    'Cuba': 'CU',
    'Cyprus': 'CY',
    'Czech Republic': 'CZ',
    'Democratic Republic of the Congo': 'CD',
    'Denmark': 'DK',
    'Djibouti': 'DJ',
    'Dominica': 'DM',
    'Dominican Republic': 'DO',
    'Ecuador': 'EC',
    'Egypt': 'EG',
    'El Salvador': 'SV',
    'Equatorial Guinea': 'GQ',
    'Eritrea': 'ER',
    'Estonia': 'EE',
    'Eswatini': 'SZ',
    'Ethiopia': 'ET',
    'Fiji': 'FJ',
    'Finland': 'FI',
    'France': 'FR',
    'Gabon': 'GA',
    'Gambia': 'GM',
    'Georgia': 'GE',
    'Germany': 'DE',
    'Ghana': 'GH',
    'Greece': 'GR',
    'Grenada': 'GD',
    'Guatemala': 'GT',
    'Guinea': 'GN',
    'Guinea-Bissau': 'GW',
    'Guyana': 'GY',
    'Haiti': 'HT',
    'Honduras': 'HN',
    'Hungary': 'HU',
    'Iceland': 'IS',
    'India': 'IN',
    'Indonesia': 'ID',
    'Iran': 'IR',
    'Iraq': 'IQ',
    'Ireland': 'IE',
    'Israel': 'IL',
    'Italy': 'IT',
    'Ivory Coast': 'CI',
    'Jamaica': 'JM',
    'Japan': 'JP',
    'Jordan': 'JO',
    'Kazakhstan': 'KZ',
    'Kenya': 'KE',
    'Kiribati': 'KI',
    'Kuwait': 'KW',
    'Kyrgyzstan': 'KG',
    'Laos': 'LA',
    'Latvia': 'LV',
    'Lebanon': 'LB',
    'Lesotho': 'LS',
    'Liberia': 'LR',
    'Libya': 'LY',
    'Liechtenstein': 'LI',
    'Lithuania': 'LT',
    'Luxembourg': 'LU',
    'Madagascar': 'MG',
    'Malawi': 'MW',
    'Malaysia': 'MY',
    'Maldives': 'MV',
    'Mali': 'ML',
    'Malta': 'MT',
    'Marshall Islands': 'MH',
    'Mauritania': 'MR',
    'Mauritius': 'MU',
    'Mexico': 'MX',
    'Micronesia': 'FM',
    'Moldova': 'MD',
    'Monaco': 'MC',
    'Mongolia': 'MN',
    'Montenegro': 'ME',
    'Morocco': 'MA',
    'Mozambique': 'MZ',
    'Myanmar': 'MM',
    'Namibia': 'NA',
    'Nauru': 'NR',
    'Nepal': 'NP',
    'Netherlands': 'NL',
    'New Zealand': 'NZ',
    'Nicaragua': 'NI',
    'Niger': 'NE',
    'Nigeria': 'NG',
    'North Korea': 'KP',
    'North Macedonia': 'MK',
    'Norway': 'NO',
    'Oman': 'OM',
    'Pakistan': 'PK',
    'Palau': 'PW',
    'Panama': 'PA',
    'Papua New Guinea': 'PG',
    'Paraguay': 'PY',
    'Peru': 'PE',
    'Philippines': 'PH',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Qatar': 'QA',
    'Romania': 'RO',
    'Russia': 'RU',
    'Rwanda': 'RW',
    'Saint Kitts and Nevis': 'KN',
    'Saint Lucia': 'LC',
    'Saint Vincent and the Grenadines': 'VC',
    'Samoa': 'WS',
    'San Marino': 'SM',
    'Sao Tome and Principe': 'ST',
    'Saudi Arabia': 'SA',
    'Senegal': 'SN',
    'Serbia': 'RS',
    'Seychelles': 'SC',
    'Sierra Leone': 'SL',
    'Singapore': 'SG',
    'Slovakia': 'SK',
    'Slovenia': 'SI',
    'Solomon Islands': 'SB',
    'Somalia': 'SO',
    'South Africa': 'ZA',
    'South Korea': 'KR',
    'South Sudan': 'SS',
    'Spain': 'ES',
    'Sri Lanka': 'LK',
    'Sudan': 'SD',
    'Suriname': 'SR',
    'Sweden': 'SE',
    'Switzerland': 'CH',
    'Syria': 'SY',
    'Taiwan': 'TW',
    'Tajikistan': 'TJ',
    'Tanzania': 'TZ',
    'Thailand': 'TH',
    'Timor-Leste': 'TL',
    'Togo': 'TG',
    'Tonga': 'TO',
    'Trinidad and Tobago': 'TT',
    'Tunisia': 'TN',
    'Turkey': 'TR',
    'Turkmenistan': 'TM',
    'Tuvalu': 'TV',
    'Uganda': 'UG',
    'Ukraine': 'UA',
    'United Arab Emirates': 'AE',
    'UK': 'GB',
    'USA': 'US',
    'Uruguay': 'UY',
    'Uzbekistan': 'UZ',
    'Vanuatu': 'VU',
    'Vatican City': 'VA',
    'Venezuela': 'VE',
    'Vietnam': 'VN',
    'Yemen': 'YE',
    'Zambia': 'ZM',
    'Zimbabwe': 'ZW'
}

# <city> input looks like "Richmond, VA, USA"
@app.route("/get-weather/<location>")
def get_weather(location):
        try:
            city = location.split(",")[0].strip()

            index_of_last_comma = location.rfind(",")
            country = location[index_of_last_comma + 1:].strip()

            city_and_country = f"{city}, {country_two_letter_code[country]}"

            global token
            url = WEATHER_BASE_URL + "appid=" + WEATHER_API_KEY + "&q=" + city_and_country
            response = requests.get(url).json()
            if "weather" not in response:
                return jsonify({"error": response["message"]})
            description = response["weather"][0]["description"]
            search_items = weather_spotify_dict.get(description, [])
            playlist = search_for_playlist(token, search_items)
            if "error" in playlist:
                token = get_token()
                playlist = search_for_playlist(token, search_items)
            return jsonify({"response": response, "search_items": search_items, "playlists": playlist["playlists"]["items"]})
        except Exception as e:
            return jsonify({"error": "Please select a valid city and country"})
        
@app.route("/auto-complete/<input>")
def auto_complete(input):
    try:
        url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input}&types=(cities)&key={GOOGLE_MAPS_KEY}'
        results = requests.get(url).json()
        descriptions_only = [location['description'] for location in results['predictions']]
        return jsonify(descriptions_only)
    except Exception as e:
        return jsonify({"error":str(e)})

@app.route("/ping")
def pingme():
    return "pinged"


if __name__ == "__main__":
    app.run(debug=True)