from flask import Flask, request, jsonify
from flask_cors import CORS
from house_scanner import find_best_city_for_house
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes
geolocator = Nominatim(user_agent="my_astrology_app")

def get_zodiac_sign(longitude):
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_index = int(longitude / 30)
    return signs[sign_index]

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    try:
        data = request.get_json()
        
        name = data.get('name', 'Unknown')
        place_of_birth = data.get('place_of_birth', 'Unknown')
        dob = data.get('dob')
        time = data.get('time')

        if not all([dob, time]):
            return jsonify({"error": "Please provide date of birth (dob) and time"}), 400

        # Parse date and time
        birth_date = datetime.strptime(dob + ' ' + time, '%d/%m/%Y %H:%M')
        
        # Convert to Julian Day
        jd = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                        birth_date.hour + birth_date.minute / 60.0)
        
        # Set ephemeris path
        swe.set_ephe_path('/usr/share/sweph/ephe')
        
        # Get latitude and longitude of birthplace
        try:
            location = geolocator.geocode(place_of_birth)
            if location:
                latitude = location.latitude
                longitude = location.longitude
            else:
                latitude = 0.0
                longitude = 0.0
        except (GeocoderTimedOut, GeocoderUnavailable):
            latitude = 0.0
            longitude = 0.0

        # Calculate planets
        planets = {}
        for planet in [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                       swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]:
            pos, _ = swe.calc_ut(jd, planet)
            planets[swe.get_planet_name(planet)] = {
                "longitude": pos[0],
                "sign": get_zodiac_sign(pos[0])
            }
        
        # Calculate Ascendant (using Placidus houses)
        cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b'P')
        ascendant = {
            "longitude": ascmc[0],
            "sign": get_zodiac_sign(ascmc[0])
        }
        planets["Ascendant"] = ascendant

        response = {
            "name": name,
            "place_of_birth": place_of_birth,
            "latitude": latitude,
            "longitude": longitude,
            "date_of_birth": dob,
            "time_of_birth": time,
            "julian_day": jd,
            "planets": planets,
            "ascendant": ascendant
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/find_city_for_house', methods=['POST'])
def find_city_for_house_endpoint():
    """
    Endpoint que recebe dados de nascimento, ano alvo e casa desejada,
    e retorna as longitudes candidatas onde o Sol cai na casa escolhida.
    """
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 
                          'target_year', 'target_house']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400
        
        result = find_best_city_for_house(
            natal_data=data,
            target_year=int(data['target_year']),
            target_house=int(data['target_house'])
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
