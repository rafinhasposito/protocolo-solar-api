from flask import Flask, request, jsonify
from flask_cors import CORS
from house_scanner import (
    find_all_cities_for_year,
    get_house_for_city,
    get_canonical_coordinates,
    get_natal_coordinates,
    search_premium_cities,
    compute_solar_return_data,
    jd_to_solar_return_info,
)

app = Flask(__name__)
CORS(app)

# =============================
# Utils
# =============================
def validate_fields(data, required_fields):
    missing = [f for f in required_fields if f not in data]
    if missing:
        return f"Campos obrigatórios faltando: {', '.join(missing)}"
    return None

def validate_year(year):
    if not (1900 <= year <= 2100):
        raise ValueError("Ano fora do limite seguro (1900-2100).")

def normalize_city(city_data):
    if not city_data: return None
    new_data = city_data.copy()
    city = new_data.get("city", "")
    country = new_data.get("country", "")
    if "display_name" not in new_data:
        new_data["display_name"] = f"{city}, {country}" if country else city
    return new_data

# =============================
# ENDPOINTS DE SEGURANÇA E AUTOCOMPLETE
# =============================
@app.route("/city_suggestions", methods=["GET"])
def city_suggestions():
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        return jsonify([])
    matches = search_premium_cities(query)
    seen = set()
    suggestions = []
    for c in matches:
        key = (c['city'], c['country'])
        if key not in seen:
            seen.add(key)
            suggestions.append({
                "city": c['city'],
                "country": c['country'],
                "display": f"{c['city']}, {c['country']}"
            })
    return jsonify(suggestions[:10])

@app.route("/resolve_city", methods=["POST"])
def resolve_city():
    data = request.get_json()
    city_name = data.get("city_name")
    country = data.get("country")
    if not city_name:
        return jsonify({"error": "city_name é obrigatório"}), 400
    try:
        coords = get_canonical_coordinates(city_name, country)
        return jsonify({"status": "resolved", "data": coords})
    except ValueError as e:
        error_msg = str(e)
        if "ambigua" in error_msg.lower():
            import ast
            try:
                options_str = error_msg.split("Opções: ")[1]
                options = ast.literal_eval(options_str)
            except Exception:
                options = []
            return jsonify({"status": "ambiguous", "options": options}), 300
        return jsonify({"status": "not_found", "message": error_msg}), 404

# =============================
# Routes
# =============================

@app.route("/find_city_for_house", methods=["POST"])
def find_city_for_house():
    try:
        data = request.get_json()
        error = validate_fields(data, [
            "name", "place_of_birth", "dob",
            "time", "target_year", "target_house"
        ])
        if error:
            return jsonify({"error": error}), 400
            
        coords_natal = get_natal_coordinates(data["place_of_birth"], data.get("birth_country"))
        data["natal_lat"] = coords_natal["lat"]
        data["natal_lon"] = coords_natal["lon"]
            
        target_year = int(data["target_year"])
        validate_year(target_year)
        target_house = int(data["target_house"])
        manifesto = data.get("intent", "")
        
        casas, _ = find_all_cities_for_year(data, target_year, manifesto)
        casa = casas.get(target_house)
        
        if not casa or not casa.get("city"):
            return jsonify({"error": "Nenhuma cidade encontrada"}), 404
            
        cidade = normalize_city(casa["city"])
        return jsonify(cidade)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/find_all_cities", methods=["POST"])
def find_all_cities():
    try:
        data = request.get_json()
        error = validate_fields(data, [
            "name", "place_of_birth", "dob",
            "time", "target_year"
        ])
        if error:
            return jsonify({"error": error}), 400
            
        coords_natal = get_natal_coordinates(data["place_of_birth"], data.get("birth_country"))
        data["natal_lat"] = coords_natal["lat"]
        data["natal_lon"] = coords_natal["lon"]

        target_year = int(data["target_year"])
        validate_year(target_year)
        manifesto = data.get("intent", "")
        
        results, astro_info = find_all_cities_for_year(data, target_year, manifesto)

        # NORMALIZAÇÃO GLOBAL PARA OS CONTINENTES DINÂMICOS E CIDADE TITULAR
        for house_id, house_data in results.items():
            if house_data.get("city"):
                house_data["city"] = normalize_city(house_data["city"])
            options = house_data.get("options", {})
            for cont_key in list(options.keys()):
                options[cont_key] = [
                    normalize_city(c) for c in options[cont_key] if c
                ]

        oraculo = ""


        return jsonify({
            "results": results,
            "oraculo": oraculo,
            "return_time_utc": astro_info.get("return_time_utc", ""),
            "return_date": astro_info.get("return_date", ""),
            "sun_sign": astro_info.get("sun_sign", ""),
            "ascendant": astro_info.get("ascendant", "")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/audit_past", methods=["POST"])
def audit_past():
    try:
        data = request.get_json()
        target_year = int(data["target_year"])
        validate_year(target_year)

        if "place_of_birth" in data:
            coords_natal = get_natal_coordinates(
                data["place_of_birth"], 
                data.get("birth_country")
            )
            data["natal_lat"] = coords_natal["lat"]
            data["natal_lon"] = coords_natal["lon"]

        cidade = data.get("past_city") or data.get("city")
        lat = data.get("past_lat")
        lon = data.get("past_lon")

        if (lat is None or lon is None) and cidade:
            coords = get_canonical_coordinates(
                cidade,
                data.get("past_country")
            )
            lat = coords["lat"]
            lon = coords["lon"]

        if lat is None or lon is None:
            return jsonify({"error": "Cidade inválida"}), 400

        casa = get_house_for_city(lat, lon, data, target_year)
        jd_return, _, sun_sign, natal_asc = compute_solar_return_data(data, target_year)
        return_date, return_time_utc = jd_to_solar_return_info(jd_return)

        nomes_casas = {
            1: "O Herói", 2: "A Prosperidade", 3: "A Voz",
            4: "A Raiz", 5: "O Criador", 6: "A Ordem",
            7: "O Elo", 8: "O Salto", 9: "A Expansão",
            10: "O Governante", 11: "O Visionário", 12: "O Silêncio"
        }

        nome_casa = nomes_casas.get(casa, f"Casa {casa}")
        oraculo = ""


        return jsonify({
            "house": casa,
            "house_name": nome_casa,
            "oraculo": oraculo,
            "lat": float(lat),
            "lon": float(lon),
            "return_date": return_date,
            "return_time_utc": return_time_utc,
            "sun_sign": sun_sign,
            "ascendant": natal_asc
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)