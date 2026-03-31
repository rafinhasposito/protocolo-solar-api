from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
from datetime import datetime
from house_scanner import (
    calculate_solar_return,
    get_house_superposition,
    find_all_cities_for_year,
    gerar_oraculo_gemini,
    get_natal_coordinates,
    parse_birth_datetime # Importado para manter o tratamento robusto de datas
)

app = Flask(__name__)
CORS(app)

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    return jsonify({"message": "Rota não implementada"}), 501

@app.route('/find_city_for_house', methods=['POST'])
def find_city_for_house_endpoint():
    try:
        data = request.get_json()
        required_fields = ['name', 'place_of_birth', 'dob', 'time', 'target_year', 'target_house']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400

        target_year = int(data['target_year'])
        if not (1900 <= target_year <= 2100):
            return jsonify({"error": "Ano astrológico fora do limite seguro (1900-2100)."}), 400

        target_house = int(data['target_house'])
        manifesto = data.get('intent', '')
        
        todas_as_casas = find_all_cities_for_year(data, target_year, manifesto)
        resultado = todas_as_casas.get(target_house)

        if resultado is None or resultado.get("city") is None:
            return jsonify({"error": "Nenhuma cidade encontrada para esta casa matemática."}), 404

        return jsonify(resultado)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
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

        target_year = int(data['target_year'])
        if not (1900 <= target_year <= 2100):
            return jsonify({"error": "Ano astrológico fora do limite seguro (1900-2100)."}), 400

        manifesto = data.get('intent', '')
        
        results = find_all_cities_for_year(data, target_year, manifesto)

        alvo_id = int(data.get('alvoId', 1))
        nome_cliente = data['name']
        prompt_mestre = data.get('prompt_mestre', '')
        
        opcoes = results.get(alvo_id, {}).get('options', {})
        cidade_ht = opcoes.get('highticket')
        cidade_ac = opcoes.get('acessivel')
        cidade_na = opcoes.get('nacional')
        
        destinos_str_list = []
        if cidade_ht: destinos_str_list.append(f"{cidade_ht['display_name']}")
        if cidade_ac: destinos_str_list.append(f"{cidade_ac['display_name']}")
        if cidade_na: destinos_str_list.append(f"{cidade_na['display_name']}")
        
        # Bloqueio de Oráculo Vazio: Devolve 404 antes de enviar para o Gemini
        if not destinos_str_list:
            return jsonify({"error": "Nenhuma cidade encontrada para esta casa matemática."}), 404
            
        cidades_destino_str = destinos_str_list[0]
        
        nomes_casas = {
            1: "O Herói", 2: "A Prosperidade", 3: "A Voz", 4: "A Raiz", 
            5: "O Criador", 6: "A Ordem", 7: "O Elo", 8: "O Salto", 
            9: "A Expansão", 10: "O Governante", 11: "O Visionário", 12: "O Silêncio"
        }
        nome_casa = nomes_casas.get(alvo_id, f"Casa {alvo_id}")
        
        oraculo_ia = gerar_oraculo_gemini(prompt_mestre, nome_cliente, manifesto, alvo_id, nome_casa, cidades_destino_str, target_year)

        return jsonify({"results": results, "oraculo": oraculo_ia})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/audit_past', methods=['POST'])
def audit_past_endpoint():
    try:
        data = request.get_json()
        cidade_passado = data.get('past_city') or data.get('city')
        target_year = int(data['target_year'])

        if not (1900 <= target_year <= 2100):
            return jsonify({"error": "Ano astrológico fora do limite seguro (1900-2100)."}), 400

        past_lat = data.get('past_lat')
        past_lon = data.get('past_lon')

        if past_lat is None or past_lon is None:
            if cidade_passado:
                past_lat, past_lon = get_natal_coordinates(cidade_passado)
            
        if past_lat is None or past_lon is None:
            return jsonify({"error": "Falha na Matrix: Não foi possível localizar as coordenadas da cidade auditada. Selecione a cidade novamente na lista."}), 400

        # Parsing unificado flexível (protege contra formatos de hora/data incorretos)
        birth_date = parse_birth_datetime(data['dob'], data['time'])
        
        jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                              birth_date.hour + birth_date.minute/60.0)
        
        jd_return = calculate_solar_return(jd_natal, target_year, birth_date.month, birth_date.day)
        
        natal_lat = data.get('natal_lat')
        natal_lon = data.get('natal_lon')
        if natal_lat is None or natal_lon is None:
            natal_lat, natal_lon = get_natal_coordinates(data['place_of_birth'])
            
        if natal_lat is None or natal_lon is None:
            return jsonify({"error": "Falha ao localizar coordenadas de nascimento. O cálculo exige exatidão extrema."}), 400

        natal_cusps, _ = swe.houses_ex(jd_natal, float(natal_lat), float(natal_lon), b'P')
        _, ascmc = swe.houses_ex(jd_return, float(past_lat), float(past_lon), b'P')
        sr_ascendant = ascmc[0]
        
        house_number = get_house_superposition(sr_ascendant, natal_cusps)

        nomes_casas = {
            1: "O Herói", 2: "A Prosperidade", 3: "A Voz", 4: "A Raiz", 
            5: "O Criador", 6: "A Ordem", 7: "O Elo", 8: "O Salto", 
            9: "A Expansão", 10: "O Governante", 11: "O Visionário", 12: "O Silêncio"
        }
        nome_casa = nomes_casas.get(house_number, f"Casa {house_number}")

        prompt_mestre = f"""Aja como Mestre Astrólogo Quântico. 
O cliente {data['name']} passou o aniversário de {target_year} em {cidade_passado}. 
A matemática ancorou o Sol na Casa {house_number} ({nome_casa}). 
Escreva uma mensagem poética e acolhedora de NO MÁXIMO 100 palavras. 
Comece com: "Quando você decidiu firmar seus passos em {cidade_passado}...".
Explique como esse arquétipo moldou o aprendizado material dele naquele ano."""
        
        oraculo_ia = gerar_oraculo_gemini(prompt_mestre, data['name'], "Auditoria", house_number, nome_casa, cidade_passado, target_year)

        return jsonify({
            "house": house_number,
            "house_name": nome_casa,
            "oraculo": oraculo_ia,
            "lat": float(past_lat),
            "lon": float(past_lon)
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Modo de produção seguro (debug=False)
    app.run(host='0.0.0.0', debug=False)
