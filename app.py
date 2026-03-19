from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
from datetime import datetime
import requests
from house_scanner import (
    calculate_solar_return,
    scan_all_houses,
    find_best_city_for_house  # se quiser manter a rota antiga
)

app = Flask(__name__)
CORS(app)

def geocode_place(place_name):
    """Obtém latitude/longitude de um local usando Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "ProtocoloSolar/1.0 (contato@seudominio.com)"}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Erro no geocoding: {e}")
    return None, None

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    # (mantenha sua função original, ou pode remover se não for usar)
    # Para simplificar, estou mantendo a original, mas você pode copiar a que já tem.
    # Coloque aqui a sua implementação existente.
    pass

@app.route('/find_city_for_house', methods=['POST'])
def find_city_for_house_endpoint():
    try:
        data = request.get_json()
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 'target_year', 'target_house']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400

        # Geocode local de nascimento
        lat_natal, lon_natal = geocode_place(data['place_of_birth'])
        if lat_natal is None:
            lat_natal = -23.5505
            lon_natal = -46.6333

        # Adicionar latitude aos dados
        data['latitude'] = lat_natal
        data['longitude'] = lon_natal

        result = find_best_city_for_house(
            natal_data=data,
            target_year=int(data['target_year']),
            target_house=int(data['target_house'])
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/find_all_cities', methods=['POST'])
def find_all_cities_endpoint():
    try:
        data = request.get_json()
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 'target_year']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400

        # Converter data/hora
        birth_date = datetime.strptime(data['dob'] + ' ' + data['time'], '%d/%m/%Y %H:%M')
        jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                              birth_date.hour + birth_date.minute/60.0)

        # Geocode local de nascimento
        lat_natal, lon_natal = geocode_place(data['place_of_birth'])
        if lat_natal is None:
            lat_natal = -23.5505

        target_year = int(data['target_year'])
        jd_return = calculate_solar_return(jd_natal, target_year)

        # Chamar a função que varre todas as casas
        results = scan_all_houses(jd_return, lat_natal, step=2.0)

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
