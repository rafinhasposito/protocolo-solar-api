import swisseph as swe
from datetime import datetime, timedelta
import os
import requests
import google.generativeai as genai
import pytz
from timezonefinder import TimezoneFinder
import logging

# ========== CONFIGURAÇÃO GERAL ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

swe.set_ephe_path('/usr/share/sweph/ephe')
tz_finder = TimezoneFinder()

# ========== ARQUÉTIPOS DAS CASAS (mantidos para eventual uso futuro) ==========
HOUSE_ARCHETYPES = {
    1: ["ação", "liderança", "iniciativa", "independência", "aventura", "esporte", "coragem", "natureza"],
    2: ["dinheiro", "segurança", "bens", "estabilidade", "luxo", "finanças", "conforto", "negócios"],
    3: ["comunicação", "vendas", "marketing", "contatos", "cultura", "estudos curtos", "movimento"],
    4: ["lar", "família", "imóveis", "raízes", "paz", "tranquilidade", "retiro", "passado"],
    5: ["romance", "criatividade", "lazer", "sorte", "diversão", "arte", "praia", "festa", "entretenimento"],
    6: ["saúde", "rotina", "trabalho", "serviço", "bem-estar", "natureza", "purificação", "organização"],
    7: ["parcerias", "casamento", "contratos", "alianças", "beleza", "diplomacia", "romance", "sociedade"],
    8: ["transformação", "herança", "renascimento", "poder", "mistério", "intensidade", "esoterismo", "crise"],
    9: ["viagens", "estudos", "expansão", "filosofia", "história", "conhecimento", "cultura", "religião"],
    10: ["carreira", "fama", "autoridade", "reconhecimento", "negócios", "metrópole", "status", "poder"],
    11: ["networking", "amigos", "projetos", "futuro", "inovação", "tecnologia", "grupos", "sociedade"],
    12: ["intuição", "espiritualidade", "isolamento", "cura", "retiro", "misticismo", "paz", "natureza"]
}

# ========== BANCO DE DADOS PREMIUM (coordenadas canônicas) ==========
PREMIUM_CITIES = [
    # ... (o mesmo conteúdo que você já tem, incluindo Buenos Aires, etc.)
    # Não repetirei aqui para economizar espaço, mas mantenha todo o banco.
    # Apenas garanta que Buenos Aires está presente:
    {"continent": "América do Sul", "country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816, "tags": ["cultura", "arte", "romance", "gastronomia"], "score": 8},
    # ... resto das cidades ...
]

# ========== FUNÇÕES AUXILIARES ==========
def parse_birth_datetime(dob_str, time_str):
    time_str = time_str.strip()
    if ':' not in time_str:
        if len(time_str) <= 2:
            time_str = f"{time_str.zfill(2)}:00"
        elif len(time_str) == 4:
            time_str = f"{time_str[:2]}:{time_str[2:]}"
        else:
            time_str = "12:00"
    else:
        parts = time_str.split(':')
        if len(parts) >= 2:
            time_str = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
    
    full_str = f"{dob_str.strip()} {time_str}"
    try:
        return datetime.strptime(full_str, '%d/%m/%Y %H:%M')
    except ValueError:
        try:
            return datetime.strptime(full_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("Formato de data/hora inválido.")

# ========== GEOCODING FALLBACK ==========
def get_natal_coordinates(city_name):
    if not city_name or city_name.strip() == "":
        raise ValueError("Nome da cidade não pode estar vazio.")
    url_photon = f"https://photon.komoot.io/api/?q={city_name}&limit=1"
    try:
        resp = requests.get(url_photon, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data and "features" in data and len(data["features"]) > 0:
                coords = data["features"][0]["geometry"]["coordinates"]
                return coords[1], coords[0]
    except Exception as e:
        logger.warning(f"Photon falhou para {city_name}: {e}")

    url_nom = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "ProtocoloSolar_ValidacaoPassagem/1.0"}
    try:
        resp = requests.get(url_nom, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        logger.warning(f"Nominatim falhou para {city_name}: {e}")

    raise ValueError(f"Não foi possível geocodificar '{city_name}'.")

def get_canonical_coordinates(city_name, country=None):
    """Retorna as coordenadas de uma cidade usando o banco PREMIUM_CITIES como fonte de verdade.
       Se não encontrar, faz geocodificação."""
    for c in PREMIUM_CITIES:
        if c['city'].lower() == city_name.lower():
            if country is None or c['country'].lower() == country.lower():
                return c['lat'], c['lon']
    # Fallback: geocodificação
    return get_natal_coordinates(city_name)

# ========== FUSO HORÁRIO ==========
def get_timezone(lat, lon):
    tz_name = tz_finder.certain_timezone_at(lat=lat, lng=lon)
    if not tz_name:
        logger.warning(f"Fuso não encontrado para lat {lat}, lon {lon}. Usando UTC.")
        return pytz.UTC
    return pytz.timezone(tz_name)

def local_to_utc(lat, lon, local_datetime):
    tz = get_timezone(lat, lon)
    try:
        local_dt = tz.localize(local_datetime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        local_dt = tz.localize(local_datetime, is_dst=False)
    except pytz.exceptions.NonExistentTimeError:
        local_dt = tz.localize(local_datetime + timedelta(hours=1), is_dst=True)
    return local_dt.astimezone(pytz.UTC)

# ========== CÁLCULOS ASTROLÓGICOS ==========
def calculate_solar_return(jd_natal, target_year, birth_month, birth_day):
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    try:
        start_date = datetime(target_year, birth_month, birth_day)
    except ValueError:
        start_date = datetime(target_year, 3, 1)
    start_date -= timedelta(days=3)
    jd_start = swe.julday(start_date.year, start_date.month, start_date.day, 12.0)
    return swe.solcross_ut(sun_longitude, jd_start)

def get_house_superposition(sr_ascendant, natal_cusps):
    for i in range(12):
        cusp_start = natal_cusps[i]
        cusp_end = natal_cusps[0] if i == 11 else natal_cusps[i+1]
        if cusp_start < cusp_end:
            if cusp_start <= sr_ascendant < cusp_end:
                return i + 1
        else:
            if sr_ascendant >= cusp_start or sr_ascendant < cusp_end:
                return i + 1
    return 1

def compute_solar_return_data(natal_data, target_year):
    """Retorna (jd_return, natal_cusps) para os dados de nascimento."""
    birth_local = parse_birth_datetime(natal_data['dob'], natal_data['time'])
    natal_lat = natal_data.get('natal_lat')
    natal_lon = natal_data.get('natal_lon')
    if natal_lat is None or natal_lon is None:
        natal_lat, natal_lon = get_canonical_coordinates(natal_data['place_of_birth'])
    natal_lat = float(natal_lat)
    natal_lon = float(natal_lon)

    birth_utc = local_to_utc(natal_lat, natal_lon, birth_local)
    jd_natal = swe.julday(birth_utc.year, birth_utc.month, birth_utc.day,
                          birth_utc.hour + birth_utc.minute / 60.0)
    jd_return = calculate_solar_return(jd_natal, int(target_year), birth_local.month, birth_local.day)
    natal_cusps, _ = swe.houses_ex(jd_natal, natal_lat, natal_lon, b'P')
    return jd_return, natal_cusps

def get_house_for_city(city_lat, city_lon, natal_data, target_year):
    """Calcula a casa ativada por uma cidade na Revolução Solar."""
    jd_return, natal_cusps = compute_solar_return_data(natal_data, target_year)
    _, ascmc = swe.houses_ex(jd_return, city_lat, city_lon, b'P')
    sr_ascendant = ascmc[0]
    return get_house_superposition(sr_ascendant, natal_cusps)

def get_city_tier(city):
    if city['country'] == 'Brasil':
        return 'nacional'
    high_ticket = [
        'EUA', 'Canadá', 'França', 'Itália', 'Reino Unido', 'Espanha',
        'Suíça', 'Alemanha', 'Emirados Árabes', 'Japão', 'Austrália',
        'Nova Zelândia', 'Mónaco', 'Vaticano', 'Holanda', 'Bélgica',
        'Islândia', 'Dinamarca', 'Suécia', 'Noruega', 'Finlândia',
        'Áustria', 'Luxemburgo', 'Singapura', 'Polinésia Francesa', 'Catar'
    ]
    if city['country'] in high_ticket:
        return 'highticket'
    return 'acessivel'

def score_city_for_house(city, house_id, user_intent):
    # Prioridade apenas ao score de fama (ignora tags e intenção)
    return city.get("score", 0)

def scan_premium_houses(jd_return, natal_cusps, user_intent=""):
    results = {i: {
        "city": None, "lat": None, "lon": None, "longitude": None,
        "options": {"highticket": None, "acessivel": None, "nacional": None}
    } for i in range(1, 13)}
    
    valid_cities_per_house = {i: [] for i in range(1, 13)}

    for city in PREMIUM_CITIES:
        _, ascmc = swe.houses_ex(jd_return, city["lat"], city["lon"], b'P')
        sr_ascendant = ascmc[0]
        house = get_house_superposition(sr_ascendant, natal_cusps)
        total_score = score_city_for_house(city, house, user_intent)
        
        city_data = {
            "city": city["city"],
            "country": city["country"],
            "continent": city["continent"],
            "display_name": f"{city['city']}, {city['country']}",
            "lat": city["lat"],
            "lon": city["lon"],
            "tier": get_city_tier(city),
            "score": total_score
        }
        valid_cities_per_house[house].append(city_data)
            
    for i in range(1, 13):
        if valid_cities_per_house[i]:
            valid_cities_per_house[i].sort(key=lambda x: x["score"], reverse=True)
            best_city = valid_cities_per_house[i][0]
            tier = best_city["tier"]
            results[i]["options"][tier] = best_city
            results[i]["city"] = best_city
            results[i]["lat"] = best_city["lat"]
            results[i]["lon"] = best_city["lon"]
            results[i]["longitude"] = best_city["lon"]

    return results

def find_all_cities_for_year(natal_data, target_year, user_intent=""):
    if not (1900 <= int(target_year) <= 2100):
        raise ValueError("Ano fora do limite seguro (1900-2100).")
    
    jd_return, natal_cusps = compute_solar_return_data(natal_data, target_year)
    return scan_premium_houses(jd_return, natal_cusps, user_intent)

# ========== GEMINI ==========
CHAVE_API = os.environ.get("GEMINI_API_KEY")
if CHAVE_API:
    genai.configure(api_key=CHAVE_API)

def gerar_oraculo_gemini(prompt_recebido, nome, manifesto, casa_id, nome_casa, cidades_destino_str, ano):
    if not CHAVE_API:
        return ""
    prompt_estrategico = prompt_recebido if prompt_recebido else f"Confirme a viagem de {nome} para ativar a Casa {casa_id}."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        resposta = model.generate_content(
            prompt_estrategico,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=150
            )
        )
        return resposta.text.replace('\n', '<br>')
    except Exception as e:
        logger.error(f"ERRO GEMINI: {e}")
        return ""
