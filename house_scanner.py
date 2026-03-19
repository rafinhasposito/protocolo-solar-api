import swisseph as swe
from datetime import datetime
import math

# ========== CONFIGURAÇÃO DA SWISS EPHEMERIS ==========
# Caminho para os ficheiros de efemérides no servidor Render
swe.set_ephe_path('/usr/share/sweph/ephe')

# ========== BANCO DE DADOS HIGH-TICKET DISTRIBUÍDO ==========
# Mais de 70 âncoras premium cobrindo os 360 graus da Terra para evitar casas vazias.
PREMIUM_CITIES = [
    # FUSOS NEGATIVOS (Américas e Pacífico)
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Bora Bora", "lat": -16.5004, "lon": -151.7415},
    {"continent": "América do Norte", "country": "EUA", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583},
    {"continent": "América do Norte", "country": "EUA", "city": "Anchorage", "lat": 61.2181, "lon": -149.9003},
    {"continent": "América do Norte", "country": "Canadá", "city": "Vancouver", "lat": 49.2827, "lon": -123.1207},
    {"continent": "América do Norte", "country": "EUA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"continent": "América do Norte", "country": "EUA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"continent": "América do Norte", "country": "México", "city": "Cidade do México", "lat": 19.4326, "lon": -99.1332},
    {"continent": "América do Norte", "country": "EUA", "city": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"continent": "América do Norte", "country": "EUA", "city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"continent": "América do Norte", "country": "México", "city": "Cancún", "lat": 21.1619, "lon": -86.8515},
    {"continent": "América do Norte", "country": "EUA", "city": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"continent": "América do Norte", "country": "Canadá", "city": "Toronto", "lat": 43.6510, "lon": -79.3470},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Iorque", "lat": 40.7128, "lon": -74.0060},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Cartagena", "lat": 10.3910, "lon": -75.4794},
    {"continent": "América do Sul", "country": "Peru", "city": "Cusco", "lat": -13.5226, "lon": -71.9673},
    {"continent": "América do Sul", "country": "Argentina", "city": "Mendoza", "lat": -32.8895, "lon": -68.8458},
    {"continent": "Caribe", "country": "República Dominicana", "city": "Punta Cana", "lat": 18.5820, "lon": -68.4055},
    {"continent": "Caribe", "country": "Bahamas", "city": "Nassau", "lat": 25.0443, "lon": -77.3504},
    {"continent": "América do Sul", "country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"continent": "América do Sul", "country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fernando de Noronha", "lat": -3.8403, "lon": -32.4297},

    # FUSOS CENTRAIS (Europa e África)
    {"continent": "Europa", "country": "Portugal (Açores)", "city": "Ponta Delgada", "lat": 37.7412, "lon": -25.6677},
    {"continent": "Europa", "country": "Islândia", "city": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
    {"continent": "África", "country": "Cabo Verde", "city": "Praia", "lat": 14.9315, "lon": -23.5125},
    {"continent": "Europa", "country": "Portugal", "city": "Lisboa", "lat": 38.7223, "lon": -9.1393},
    {"continent": "Europa", "country": "Irlanda", "city": "Dublin", "lat": 53.3498, "lon": -6.2603},
    {"continent": "África", "country": "Marrocos", "city": "Marraquexe", "lat": 31.6295, "lon": -7.9811},
    {"continent": "Europa", "country": "Espanha", "city": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"continent": "Europa", "country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"continent": "Europa", "country": "Espanha", "city": "Ibiza", "lat": 38.9067, "lon": 1.4206},
    {"continent": "Europa", "country": "França", "city": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"continent": "Europa", "country": "França", "city": "Cannes", "lat": 43.5528, "lon": 7.0174},
    {"continent": "Europa", "country": "Holanda", "city": "Amesterdão", "lat": 52.3676, "lon": 4.9041},
    {"continent": "Europa", "country": "Suíça", "city": "Zurique", "lat": 47.3769, "lon": 8.5417},
    {"continent": "Europa", "country": "Itália", "city": "Roma", "lat": 41.9028, "lon": 12.4964},
    {"continent": "Europa", "country": "Mónaco", "city": "Monte Carlo", "lat": 43.7384, "lon": 7.4246},
    {"continent": "Europa", "country": "Itália", "city": "Veneza", "lat": 45.4408, "lon": 12.3155},
    {"continent": "Europa", "country": "Alemanha", "city": "Berlim", "lat": 52.5200, "lon": 13.4050},
    {"continent": "África", "country": "África do Sul", "city": "Cidade do Cabo", "lat": -33.9249, "lon": 18.4241},
    {"continent": "Europa", "country": "Grécia", "city": "Atenas", "lat": 37.9838, "lon": 23.7275},
    {"continent": "Europa", "country": "Grécia", "city": "Santorini", "lat": 36.3932, "lon": 25.4615},
    {"continent": "Europa", "country": "Turquia", "city": "Istambul", "lat": 41.0082, "lon": 28.9784},
    {"continent": "África", "country": "Egito", "city": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"continent": "Europa", "country": "Rússia", "city": "Moscovo", "lat": 55.7558, "lon": 37.6173},
    
    # FUSOS POSITIVOS (Médio Oriente, Ásia, Oceania)
    {"continent": "Médio Oriente", "country": "Catar", "city": "Doha", "lat": 25.2854, "lon": 51.5310},
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Dubai", "lat": 25.2048, "lon": 55.2708},
    {"continent": "África", "country": "Seychelles", "city": "Mahé", "lat": -4.6796, "lon": 55.4920},
    {"continent": "África", "country": "Maurícia", "city": "Port Louis", "lat": -20.1609, "lon": 57.5012},
    {"continent": "Ásia", "country": "Maldivas", "city": "Malé", "lat": 4.1755, "lon": 73.5093},
    {"continent": "Ásia", "country": "Índia", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"continent": "Ásia", "country": "Índia", "city": "Nova Deli", "lat": 28.6139, "lon": 77.2090},
    {"continent": "Ásia", "country": "Tailândia", "city": "Phuket", "lat": 7.8804, "lon": 98.3922},
    {"continent": "Ásia", "country": "Tailândia", "city": "Banguecoque", "lat": 13.7563, "lon": 100.5018},
    {"continent": "Ásia", "country": "Singapura", "city": "Singapura", "lat": 1.3521, "lon": 103.8198},
    {"continent": "Ásia", "country": "China", "city": "Pequim", "lat": 39.9042, "lon": 116.4074},
    {"continent": "Ásia", "country": "Indonésia", "city": "Bali", "lat": -8.4095, "lon": 115.1889},
    {"continent": "Ásia", "country": "China", "city": "Xangai", "lat": 31.2304, "lon": 121.4737},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Seul", "lat": 37.5665, "lon": 126.9780},
    {"continent": "Ásia", "country": "Japão", "city": "Quioto", "lat": 35.0116, "lon": 135.7681},
    {"continent": "Ásia", "country": "Japão", "city": "Tóquio", "lat": 35.6762, "lon": 139.6503},
    {"continent": "Oceania", "country": "Austrália", "city": "Melbourne", "lat": -37.8136, "lon": 144.9631},
    {"continent": "Oceania", "country": "Austrália", "city": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Auckland", "lat": -36.8485, "lon": 174.7633},
    {"continent": "Oceania", "country": "Fiji", "city": "Nadi", "lat": -17.8065, "lon": 177.4136}
]

def calculate_solar_return(jd_natal, target_year):
    """Calcula o momento exato do Retorno Solar."""
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    jd_start = swe.julday(target_year, 1, 1, 12.0)
    return swe.solcross_ut(sun_longitude, jd_start)

def calculate_house_position(jd_ut, longitude, latitude):
    """Verifica a Casa Astrológica com precisão corrigida para a matriz da Swiss Ephemeris."""
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    sun_pos, _ = swe.calc_ut(jd_ut, swe.SUN)
    sun_lon = sun_pos[0]
    
    # A Swiss Ephemeris usa índices de 1 a 12 para as casas (índice 0 é nulo)
    for i in range(1, 13):
        cusp_start = cusps[i]
        cusp_end = cusps[1] if i == 12 else cusps[i+1]
        
        # O círculo do zodíaco tem 360 graus. Se a casa cruzar o ponto zero (Áries), 
        # a lógica matemática precisa inverter para não quebrar.
        if cusp_start < cusp_end:
            if cusp_start <= sun_lon < cusp_end:
                return i
        else:
            # Atravessa o grau 360 (Ex: Casa começa no grau 350 e termina no grau 10)
            if sun_lon >= cusp_start or sun_lon < cusp_end:
                return i
                
    return 1 # Fallback de segurança quântica

def scan_premium_houses(jd_return):
    """
    Algoritmo High-Ticket:
    Preenche as 12 cartas do cliente apenas com destinos luxuosos.
    Garante que um país não se repita para criar um roteiro diversificado.
    """
    results = {i: None for i in range(1, 13)}
    used_countries = set()
    
    # PASSAGEM 1: Exclusividade Máxima (Sem repetir países)
    for city in PREMIUM_CITIES:
        house = calculate_house_position(jd_return, city["lon"], city["lat"])
        
        if results[house] is None and city["country"] not in used_countries:
            results[house] = {
                "city": {
                    "city": city["city"],
                    "country": city["country"],
                    "continent": city["continent"],
                    "display_name": f"{city['city']}, {city['country']}"
                },
                "longitude": city["lon"]
            }
            used_countries.add(city["country"])
            
    # PASSAGEM 2: Preenchimento de Fendas Quânticas (Fallback)
    # Se uma casa astrológica for extremamente estreita naquele ano, preenchemos com o
    # destino tático mais próximo, mesmo que repita o país, para não entregar carta nula.
    for i in range(1, 13):
        if results[i] is None:
            for city in PREMIUM_CITIES:
                house = calculate_house_position(jd_return, city["lon"], city["lat"])
                if house == i:
                    results[i] = {
                        "city": {
                            "city": city["city"],
                            "country": city["country"],
                            "continent": city["continent"],
                            "display_name": f"{city['city']}, {city['country']} (Ancoragem Expandida)"
                        },
                        "longitude": city["lon"]
                    }
                    break
                    
    return results

def find_all_cities_for_year(natal_data, target_year):
    """Ponte de comunicação com a API."""
    try:
        birth_date = datetime.strptime(natal_data['dob'] + ' ' + natal_data['time'], '%d/%m/%Y %H:%M')
        jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                              birth_date.hour + birth_date.minute/60.0)
                              
        jd_return = calculate_solar_return(jd_natal, target_year)
        
        return scan_premium_houses(jd_return)
        
    except Exception as e:
        print(f"Erro Crítico de Astrocartografia: {e}")
        raise e
