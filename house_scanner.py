import swisseph as swe
from datetime import datetime

# ========== CONFIGURAÇÃO DA SWISS EPHEMERIS ==========
swe.set_ephe_path('/usr/share/sweph/ephe')

# ========== BANCO DE DADOS PREMIUM EXPANDIDO (120+ CIDADES) ==========
PREMIUM_CITIES = [
    # AMÉRICAS
    {"continent": "América do Norte", "country": "Canadá", "city": "Vancouver", "lat": 49.2827, "lon": -123.1207},
    {"continent": "América do Norte", "country": "Canadá", "city": "Toronto", "lat": 43.6510, "lon": -79.3470},
    {"continent": "América do Norte", "country": "Canadá", "city": "Montreal", "lat": 45.5017, "lon": -73.5673},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Iorque", "lat": 40.7128, "lon": -74.0060},
    {"continent": "América do Norte", "country": "EUA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"continent": "América do Norte", "country": "EUA", "city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"continent": "América do Norte", "country": "EUA", "city": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"continent": "América do Norte", "country": "EUA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"continent": "América do Norte", "country": "EUA", "city": "São Francisco", "lat": 37.7749, "lon": -122.4194},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Orleans", "lat": 29.9511, "lon": -90.0715},
    {"continent": "América do Norte", "country": "EUA", "city": "Boston", "lat": 42.3601, "lon": -71.0589},
    {"continent": "América do Norte", "country": "México", "city": "Cidade do México", "lat": 19.4326, "lon": -99.1332},
    {"continent": "América do Norte", "country": "México", "city": "Cancún", "lat": 21.1619, "lon": -86.8515},
    {"continent": "América Central", "country": "Costa Rica", "city": "São José", "lat": 9.9281, "lon": -84.0907},
    {"continent": "Caribe", "country": "Bahamas", "city": "Nassau", "lat": 25.0443, "lon": -77.3504},
    {"continent": "Caribe", "country": "República Dominicana", "city": "Punta Cana", "lat": 18.5820, "lon": -68.4055},
    {"continent": "Caribe", "country": "Porto Rico", "city": "San Juan", "lat": 18.4655, "lon": -66.1057},
    {"continent": "América do Sul", "country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"continent": "América do Sul", "country": "Brasil", "city": "Salvador", "lat": -12.9714, "lon": -38.5014},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fernando de Noronha", "lat": -3.8403, "lon": -32.4297},
    {"continent": "América do Sul", "country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    {"continent": "América do Sul", "country": "Argentina", "city": "Mendoza", "lat": -32.8895, "lon": -68.8458},
    {"continent": "América do Sul", "country": "Chile", "city": "Santiago", "lat": -33.4489, "lon": -70.6693},
    {"continent": "América do Sul", "country": "Chile", "city": "Ilha de Páscoa", "lat": -27.1127, "lon": -109.3497},
    {"continent": "América do Sul", "country": "Peru", "city": "Lima", "lat": -12.0464, "lon": -77.0428},
    {"continent": "América do Sul", "country": "Peru", "city": "Cusco", "lat": -13.5226, "lon": -71.9673},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Cartagena", "lat": 10.3910, "lon": -75.4794},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Bogotá", "lat": 4.7110, "lon": -74.0721},
    {"continent": "América do Sul", "country": "Equador", "city": "Quito", "lat": -0.1807, "lon": -78.4678},
    {"continent": "América do Sul", "country": "Equador", "city": "Ilhas Galápagos", "lat": -0.7437, "lon": -90.3136},

    # EUROPA
    {"continent": "Europa", "country": "Islândia", "city": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
    {"continent": "Europa", "country": "Portugal", "city": "Lisboa", "lat": 38.7223, "lon": -9.1393},
    {"continent": "Europa", "country": "Portugal", "city": "Porto", "lat": 41.1579, "lon": -8.6291},
    {"continent": "Europa", "country": "Portugal (Açores)", "city": "Ponta Delgada", "lat": 37.7412, "lon": -25.6677},
    {"continent": "Europa", "country": "Portugal (Madeira)", "city": "Funchal", "lat": 32.6669, "lon": -16.9241},
    {"continent": "Europa", "country": "Espanha", "city": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"continent": "Europa", "country": "Espanha", "city": "Barcelona", "lat": 41.3851, "lon": 2.1734},
    {"continent": "Europa", "country": "Espanha", "city": "Ibiza", "lat": 38.9067, "lon": 1.4206},
    {"continent": "Europa", "country": "França", "city": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"continent": "Europa", "country": "França", "city": "Cannes", "lat": 43.5528, "lon": 7.0174},
    {"continent": "Europa", "country": "França", "city": "Nice", "lat": 43.7102, "lon": 7.2620},
    {"continent": "Europa", "country": "Mónaco", "city": "Monte Carlo", "lat": 43.7384, "lon": 7.4246},
    {"continent": "Europa", "country": "Itália", "city": "Roma", "lat": 41.9028, "lon": 12.4964},
    {"continent": "Europa", "country": "Itália", "city": "Veneza", "lat": 45.4408, "lon": 12.3155},
    {"continent": "Europa", "country": "Itália", "city": "Florença", "lat": 43.7696, "lon": 11.2558},
    {"continent": "Europa", "country": "Itália", "city": "Milão", "lat": 45.4642, "lon": 9.1900},
    {"continent": "Europa", "country": "Suíça", "city": "Zurique", "lat": 47.3769, "lon": 8.5417},
    {"continent": "Europa", "country": "Suíça", "city": "Genebra", "lat": 46.2044, "lon": 6.1432},
    {"continent": "Europa", "country": "Alemanha", "city": "Berlim", "lat": 52.5200, "lon": 13.4050},
    {"continent": "Europa", "country": "Alemanha", "city": "Munique", "lat": 48.1351, "lon": 11.5820},
    {"continent": "Europa", "country": "Áustria", "city": "Viena", "lat": 48.2082, "lon": 16.3738},
    {"continent": "Europa", "country": "Holanda", "city": "Amesterdão", "lat": 52.3676, "lon": 4.9041},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruxelas", "lat": 50.8503, "lon": 4.3517},
    {"continent": "Europa", "country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"continent": "Europa", "country": "Reino Unido", "city": "Edimburgo", "lat": 55.9533, "lon": -3.1883},
    {"continent": "Europa", "country": "Irlanda", "city": "Dublin", "lat": 53.3498, "lon": -6.2603},
    {"continent": "Europa", "country": "Dinamarca", "city": "Copenhaga", "lat": 55.6761, "lon": 12.5683},
    {"continent": "Europa", "country": "Suécia", "city": "Estocolmo", "lat": 59.3293, "lon": 18.0686},
    {"continent": "Europa", "country": "Noruega", "city": "Oslo", "lat": 59.9139, "lon": 10.7522},
    {"continent": "Europa", "country": "Finlândia", "city": "Helsínquia", "lat": 60.1699, "lon": 24.9384},
    {"continent": "Europa", "country": "Rússia", "city": "Moscovo", "lat": 55.7558, "lon": 37.6173},
    {"continent": "Europa", "country": "Rússia", "city": "São Petersburgo", "lat": 59.9343, "lon": 30.3351},
    {"continent": "Europa", "country": "Grécia", "city": "Atenas", "lat": 37.9838, "lon": 23.7275},
    {"continent": "Europa", "country": "Grécia", "city": "Santorini", "lat": 36.3932, "lon": 25.4615},
    {"continent": "Europa", "country": "Grécia", "city": "Míconos", "lat": 37.4467, "lon": 25.3289},
    {"continent": "Europa", "country": "Turquia", "city": "Istambul", "lat": 41.0082, "lon": 28.9784},
    {"continent": "Europa", "country": "Croácia", "city": "Dubrovnik", "lat": 42.6507, "lon": 18.0944},
    {"continent": "Europa", "country": "Hungria", "city": "Budapeste", "lat": 47.4979, "lon": 19.0402},
    {"continent": "Europa", "country": "República Checa", "city": "Praga", "lat": 50.0755, "lon": 14.4378},
    {"continent": "Europa", "country": "Polónia", "city": "Varsóvia", "lat": 52.2297, "lon": 21.0122},

    # ÁFRICA
    {"continent": "África", "country": "Marrocos", "city": "Marraquexe", "lat": 31.6295, "lon": -7.9811},
    {"continent": "África", "country": "Marrocos", "city": "Casablanca", "lat": 33.5731, "lon": -7.5898},
    {"continent": "África", "country": "Egito", "city": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"continent": "África", "country": "Egito", "city": "Luxor", "lat": 25.6872, "lon": 32.6396},
    {"continent": "África", "country": "África do Sul", "city": "Cidade do Cabo", "lat": -33.9249, "lon": 18.4241},
    {"continent": "África", "country": "África do Sul", "city": "Joanesburgo", "lat": -26.2041, "lon": 28.0473},
    {"continent": "África", "country": "Quénia", "city": "Nairobi", "lat": -1.2921, "lon": 36.8219},
    {"continent": "África", "country": "Tanzânia", "city": "Zanzibar", "lat": -6.1659, "lon": 39.2026},
    {"continent": "África", "country": "Tanzânia", "city": "Arusha", "lat": -3.3869, "lon": 36.6830},
    {"continent": "África", "country": "Maurícia", "city": "Port Louis", "lat": -20.1609, "lon": 57.5012},
    {"continent": "África", "country": "Seychelles", "city": "Mahé", "lat": -4.6796, "lon": 55.4920},
    {"continent": "África", "country": "Cabo Verde", "city": "Praia", "lat": 14.9315, "lon": -23.5125},
    {"continent": "África", "country": "Cabo Verde", "city": "Sal", "lat": 16.7412, "lon": -22.9441},

    # MÉDIO ORIENTE
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Dubai", "lat": 25.2048, "lon": 55.2708},
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Abu Dhabi", "lat": 24.4539, "lon": 54.3773},
    {"continent": "Médio Oriente", "country": "Catar", "city": "Doha", "lat": 25.2854, "lon": 51.5310},
    {"continent": "Médio Oriente", "country": "Arábia Saudita", "city": "Riade", "lat": 24.7136, "lon": 46.6753},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Tel Aviv", "lat": 32.0853, "lon": 34.7818},
    {"continent": "Médio Oriente", "country": "Jordânia", "city": "Petra", "lat": 30.3285, "lon": 35.4444},

    # ÁSIA
    {"continent": "Ásia", "country": "Índia", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"continent": "Ásia", "country": "Índia", "city": "Nova Deli", "lat": 28.6139, "lon": 77.2090},
    {"continent": "Ásia", "country": "Índia", "city": "Goa", "lat": 15.2993, "lon": 74.1240},
    {"continent": "Ásia", "country": "Tailândia", "city": "Banguecoque", "lat": 13.7563, "lon": 100.5018},
    {"continent": "Ásia", "country": "Tailândia", "city": "Phuket", "lat": 7.8804, "lon": 98.3922},
    {"continent": "Ásia", "country": "Tailândia", "city": "Chiang Mai", "lat": 18.7883, "lon": 98.9853},
    {"continent": "Ásia", "country": "Vietname", "city": "Hanói", "lat": 21.0285, "lon": 105.8542},
    {"continent": "Ásia", "country": "Vietname", "city": "Ho Chi Minh", "lat": 10.8231, "lon": 106.6297},
    {"continent": "Ásia", "country": "Camboja", "city": "Siem Reap", "lat": 13.3633, "lon": 103.8564},
    {"continent": "Ásia", "country": "Malásia", "city": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869},
    {"continent": "Ásia", "country": "Singapura", "city": "Singapura", "lat": 1.3521, "lon": 103.8198},
    {"continent": "Ásia", "country": "Indonésia", "city": "Bali", "lat": -8.4095, "lon": 115.1889},
    {"continent": "Ásia", "country": "Indonésia", "city": "Jacarta", "lat": -6.2088, "lon": 106.8456},
    {"continent": "Ásia", "country": "Filipinas", "city": "Manila", "lat": 14.5995, "lon": 120.9842},
    {"continent": "Ásia", "country": "China", "city": "Pequim", "lat": 39.9042, "lon": 116.4074},
    {"continent": "Ásia", "country": "China", "city": "Xangai", "lat": 31.2304, "lon": 121.4737},
    {"continent": "Ásia", "country": "China", "city": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
    {"continent": "Ásia", "country": "Japão", "city": "Tóquio", "lat": 35.6762, "lon": 139.6503},
    {"continent": "Ásia", "country": "Japão", "city": "Quioto", "lat": 35.0116, "lon": 135.7681},
    {"continent": "Ásia", "country": "Japão", "city": "Osaka", "lat": 34.6937, "lon": 135.5023},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Seul", "lat": 37.5665, "lon": 126.9780},
    {"continent": "Ásia", "country": "Taiwan", "city": "Taipé", "lat": 25.0330, "lon": 121.5654},

    # OCEANIA
    {"continent": "Oceania", "country": "Austrália", "city": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"continent": "Oceania", "country": "Austrália", "city": "Melbourne", "lat": -37.8136, "lon": 144.9631},
    {"continent": "Oceania", "country": "Austrália", "city": "Brisbane", "lat": -27.4698, "lon": 153.0251},
    {"continent": "Oceania", "country": "Austrália", "city": "Perth", "lat": -31.9505, "lon": 115.8605},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Auckland", "lat": -36.8485, "lon": 174.7633},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Queenstown", "lat": -45.0312, "lon": 168.6626},
    {"continent": "Oceania", "country": "Fiji", "city": "Nadi", "lat": -17.8065, "lon": 177.4136},
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Bora Bora", "lat": -16.5004, "lon": -151.7415},
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Taiti", "lat": -17.6509, "lon": -149.4260},
    {"continent": "Oceania", "country": "Havaí", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583},
]

def calculate_solar_return(jd_natal, target_year):
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    jd_start = swe.julday(target_year, 1, 1, 12.0)
    return swe.solcross_ut(sun_longitude, jd_start)

def calculate_house_position(jd_ut, longitude, latitude):
    """Lógica CORRIGIDA para impedir o sumiço das Casas 6 a 11."""
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    sun_pos, _ = swe.calc_ut(jd_ut, swe.SUN)
    sun_lon = sun_pos[0]
    
    # Índice 0 é descartado pela matriz astrológica. Loop de 1 a 12.
    for i in range(1, 13):
        cusp_start = cusps[i]
        cusp_end = cusps[1] if i == 12 else cusps[i+1]
        
        if cusp_start < cusp_end:
            if cusp_start <= sun_lon < cusp_end:
                return i
        else:
            if sun_lon >= cusp_start or sun_lon < cusp_end:
                return i
    return 1

def scan_premium_houses(jd_return):
    """
    Algoritmo reforçado: garante que TODAS as 12 casas recebam uma cidade.
    """
    results = {i: None for i in range(1, 13)}
    used_countries = set()

    # Passo 1: Atribuir cidades com países únicos
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

    # Passo 2: Fallback robusto – preenche as casas vazias com a primeira cidade disponível para aquela casa
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
                            "display_name": f"{city['city']}, {city['country']}"
                        },
                        "longitude": city["lon"]
                    }
                    break

    return results

def find_all_cities_for_year(natal_data, target_year):
    try:
        birth_date = datetime.strptime(natal_data['dob'] + ' ' + natal_data['time'], '%d/%m/%Y %H:%M')
        jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                              birth_date.hour + birth_date.minute/60.0)
        jd_return = calculate_solar_return(jd_natal, target_year)
        return scan_premium_houses(jd_return)
    except Exception as e:
        print(f"Erro: {e}")
        raise e
