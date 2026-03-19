from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
from datetime import datetime
import requests
from house_scanner import (
    calculate_solar_return,
    find_all_cities_for_year   # função principal que retorna todas as casas
)

app = Flask(__name__)
CORS(app)

def geocode_place(place_name):
    """Obtém latitude/longitude de um local usando Nominatim (usado apenas para local de nascimento)."""
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
    # Se você não usa essa rota, pode remover ou manter como stub
    return jsonify({"message": "Rota não implementada"}), 501

@app.route('/find_city_for_house', methods=['POST'])
def find_city_for_house_endpoint():
    """
    Rota mantida para compatibilidade com versões anteriores.
    Retorna apenas a cidade da casa solicitada.
    """
    try:
        data = request.get_json()
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 'target_year', 'target_house']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400

        target_year = int(data['target_year'])
        target_house = int(data['target_house'])

        # Usa a função principal para obter todas as casas
        todas_as_casas = find_all_cities_for_year(data, target_year)

        # Extrai a casa desejada
        resultado = todas_as_casas.get(target_house)

        if resultado is None:
            return jsonify({"error": "Nenhuma cidade encontrada para esta casa"}), 404

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/find_all_cities', methods=['POST'])
def find_all_cities_endpoint():
    """
    Nova rota que retorna as cidades para todas as 12 casas de uma só vez.
    """
    try:
        data = request.get_json()
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 'target_year']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400

        target_year = int(data['target_year'])

        # Chama a função principal do motor premium
        results = find_all_cities_for_year(data, target_year)

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
