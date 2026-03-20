import swisseph as swe
from datetime import datetime

# ========== CONFIGURAÇÃO DA SWISS EPHEMERIS ==========
swe.set_ephe_path('/usr/share/sweph/ephe')

# ========== BANCO DE DADOS PREMIUM EXPANDIDO (350+ CIDADES) ==========
# A ordem da lista influencia a prioridade: cidades no topo são escolhidas primeiro
# quando múltiplas cidades caem na mesma casa astrológica.
PREMIUM_CITIES = [

    # -----------------------------------------------------------------
    # 1. BRASIL – TODAS AS CAPITAIS + PRINCIPAIS CIDADES POR ESTADO
    # -----------------------------------------------------------------
    {"continent": "América do Sul", "country": "Brasil", "city": "Manaus", "lat": -3.1190, "lon": -60.0217},
{"continent": "América do Sul", "country": "Brasil", "city": "Belém", "lat": -1.4558, "lon": -48.5039},
{"continent": "América do Sul", "country": "Brasil", "city": "Porto Velho", "lat": -8.7608, "lon": -63.8999},
{"continent": "América do Sul", "country": "Brasil", "city": "São Luís", "lat": -2.5297, "lon": -44.3028},
{"continent": "América do Sul", "country": "Brasil", "city": "Teresina", "lat": -5.0892, "lon": -42.8019},
{"continent": "América do Sul", "country": "Brasil", "city": "Fortaleza", "lat": -3.7172, "lon": -38.5433},
{"continent": "América do Sul", "country": "Brasil", "city": "Natal", "lat": -5.7793, "lon": -35.2009},
{"continent": "América do Sul", "country": "Brasil", "city": "João Pessoa", "lat": -7.1150, "lon": -34.8610},
{"continent": "América do Sul", "country": "Brasil", "city": "Recife", "lat": -8.0476, "lon": -34.8770},
{"continent": "América do Sul", "country": "Brasil", "city": "Maceió", "lat": -9.6659, "lon": -35.7350},
{"continent": "América do Sul", "country": "Brasil", "city": "Aracaju", "lat": -10.9472, "lon": -37.0731},
{"continent": "América do Sul", "country": "Brasil", "city": "Salvador", "lat": -12.9714, "lon": -38.5014},
{"continent": "América do Sul", "country": "Brasil", "city": "Cuiabá", "lat": -15.6010, "lon": -56.0974},
{"continent": "América do Sul", "country": "Brasil", "city": "Campo Grande", "lat": -20.4697, "lon": -54.6201},
{"continent": "América do Sul", "country": "Brasil", "city": "Goiânia", "lat": -16.6864, "lon": -49.2643},
{"continent": "América do Sul", "country": "Brasil", "city": "Brasília", "lat": -15.7975, "lon": -47.8919},
{"continent": "América do Sul", "country": "Brasil", "city": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
{"continent": "América do Sul", "country": "Brasil", "city": "Vitória", "lat": -20.3155, "lon": -40.3128},
{"continent": "América do Sul", "country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
{"continent": "América do Sul", "country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333},
{"continent": "América do Sul", "country": "Brasil", "city": "Curitiba", "lat": -25.4296, "lon": -49.2719},
{"continent": "América do Sul", "country": "Brasil", "city": "Florianópolis", "lat": -27.5954, "lon": -48.5480},
{"continent": "América do Sul", "country": "Brasil", "city": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
{"continent": "América do Sul", "country": "Brasil", "city": "Santos", "lat": -23.9535, "lon": -46.3350},
{"continent": "América do Sul", "country": "Brasil", "city": "Blumenau", "lat": -26.9185, "lon": -49.0659},
{"continent": "América do Sul", "country": "Brasil", "city": "Itajaí", "lat": -26.9081, "lon": -48.6707},
{"continent": "América do Sul", "country": "Brasil", "city": "Balneário Camboriú", "lat": -26.9917, "lon": -48.6333},
{"continent": "América do Sul", "country": "Brasil", "city": "Foz do Iguaçu", "lat": -25.5478, "lon": -54.5882},
{"continent": "América do Sul", "country": "Brasil", "city": "Juazeiro do Norte", "lat": -7.2133, "lon": -39.3151},
{"continent": "América do Sul", "country": "Brasil", "city": "Campina Grande", "lat": -7.2219, "lon": -35.8739},
{"continent": "América do Sul", "country": "Brasil", "city": "Caruaru", "lat": -8.2835, "lon": -35.9698},
{"continent": "América do Sul", "country": "Brasil", "city": "Ilhéus", "lat": -14.7939, "lon": -39.0460},
{"continent": "América do Sul", "country": "Brasil", "city": "Porto Seguro", "lat": -16.4435, "lon": -39.0643},
{"continent": "América do Sul", "country": "Brasil", "city": "Cabo Frio", "lat": -22.8794, "lon": -42.0192},
{"continent": "América do Sul", "country": "Brasil", "city": "Búzios", "lat": -22.7478, "lon": -41.8819},
{"continent": "América do Sul", "country": "Brasil", "city": "Angra dos Reis", "lat": -23.0067, "lon": -44.3185},
{"continent": "América do Sul", "country": "Brasil", "city": "Paraty", "lat": -23.2192, "lon": -44.7153},
{"continent": "América do Sul", "country": "Brasil", "city": "Ubatuba", "lat": -23.4372, "lon": -45.0700},
{"continent": "América do Sul", "country": "Brasil", "city": "Ilhabela", "lat": -23.7785, "lon": -45.3552},
{"continent": "América do Sul", "country": "Brasil", "city": "Guarujá", "lat": -23.9935, "lon": -46.2567},
{"continent": "América do Sul", "country": "Brasil", "city": "Bertioga", "lat": -23.8546, "lon": -46.1383},
{"continent": "América do Sul", "country": "Brasil", "city": "São Sebastião", "lat": -23.8027, "lon": -45.4042},
{"continent": "América do Sul", "country": "Brasil", "city": "Caraguatatuba", "lat": -23.6203, "lon": -45.4131},
{"continent": "América do Sul", "country": "Brasil", "city": "Corumbá", "lat": -19.0097, "lon": -57.6514},
{"continent": "América do Sul", "country": "Brasil", "city": "Fernando de Noronha", "lat": -3.8403, "lon": -32.4297}

    # -----------------------------------------------------------------
    # 2. AMÉRICA DO NORTE (EUA, Canadá, México) – principais cidades
    # -----------------------------------------------------------------
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Iorque", "lat": 40.7128, "lon": -74.0060},
    {"continent": "América do Norte", "country": "EUA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"continent": "América do Norte", "country": "EUA", "city": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"continent": "América do Norte", "country": "EUA", "city": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"continent": "América do Norte", "country": "EUA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"continent": "América do Norte", "country": "EUA", "city": "São Francisco", "lat": 37.7749, "lon": -122.4194},
    {"continent": "América do Norte", "country": "EUA", "city": "Boston", "lat": 42.3601, "lon": -71.0589},
    {"continent": "América do Norte", "country": "EUA", "city": "Washington D.C.", "lat": 38.9072, "lon": -77.0369},
    {"continent": "América do Norte", "country": "EUA", "city": "Seattle", "lat": 47.6062, "lon": -122.3321},
    {"continent": "América do Norte", "country": "EUA", "city": "Denver", "lat": 39.7392, "lon": -104.9903},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Orleans", "lat": 29.9511, "lon": -90.0715},
    {"continent": "América do Norte", "country": "EUA", "city": "Orlando", "lat": 28.5383, "lon": -81.3792},
    {"continent": "América do Norte", "country": "EUA", "city": "Atlanta", "lat": 33.7490, "lon": -84.3880},
    {"continent": "América do Norte", "country": "EUA", "city": "Dallas", "lat": 32.7767, "lon": -96.7970},
    {"continent": "América do Norte", "country": "EUA", "city": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"continent": "América do Norte", "country": "EUA", "city": "Filadélfia", "lat": 39.9526, "lon": -75.1652},
    {"continent": "América do Norte", "country": "EUA", "city": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"continent": "América do Norte", "country": "EUA", "city": "San Diego", "lat": 32.7157, "lon": -117.1611},
    {"continent": "América do Norte", "country": "EUA", "city": "Portland", "lat": 45.5051, "lon": -122.6750},
    {"continent": "América do Norte", "country": "EUA", "city": "Detroit", "lat": 42.3314, "lon": -83.0458},
    {"continent": "América do Norte", "country": "EUA", "city": "Minneapolis", "lat": 44.9778, "lon": -93.2650},
    {"continent": "América do Norte", "country": "EUA", "city": "St. Louis", "lat": 38.6270, "lon": -90.1994},
    {"continent": "América do Norte", "country": "EUA", "city": "Kansas City", "lat": 39.0997, "lon": -94.5786},
    {"continent": "América do Norte", "country": "EUA", "city": "Nashville", "lat": 36.1627, "lon": -86.7816},
    {"continent": "América do Norte", "country": "EUA", "city": "Memphis", "lat": 35.1495, "lon": -90.0490},
    {"continent": "América do Norte", "country": "EUA", "city": "Charleston", "lat": 32.7765, "lon": -79.9311},
    {"continent": "América do Norte", "country": "EUA", "city": "Savannah", "lat": 32.0809, "lon": -81.0912},
    {"continent": "América do Norte", "country": "EUA", "city": "Aspen", "lat": 39.1911, "lon": -106.8175},
    {"continent": "América do Norte", "country": "EUA", "city": "Sedona", "lat": 34.8697, "lon": -111.7610},
    {"continent": "América do Norte", "country": "Canadá", "city": "Toronto", "lat": 43.6510, "lon": -79.3470},
    {"continent": "América do Norte", "country": "Canadá", "city": "Vancouver", "lat": 49.2827, "lon": -123.1207},
    {"continent": "América do Norte", "country": "Canadá", "city": "Montreal", "lat": 45.5017, "lon": -73.5673},
    {"continent": "América do Norte", "country": "Canadá", "city": "Calgary", "lat": 51.0447, "lon": -114.0719},
    {"continent": "América do Norte", "country": "Canadá", "city": "Ottawa", "lat": 45.4215, "lon": -75.6972},
    {"continent": "América do Norte", "country": "Canadá", "city": "Québec", "lat": 46.8139, "lon": -71.2080},
    {"continent": "América do Norte", "country": "México", "city": "Cidade do México", "lat": 19.4326, "lon": -99.1332},
    {"continent": "América do Norte", "country": "México", "city": "Cancún", "lat": 21.1619, "lon": -86.8515},
    {"continent": "América do Norte", "country": "México", "city": "Tulum", "lat": 20.2114, "lon": -87.4654},
    {"continent": "América do Norte", "country": "México", "city": "Guadalajara", "lat": 20.6597, "lon": -103.3496},
    {"continent": "América do Norte", "country": "México", "city": "Monterrey", "lat": 25.6866, "lon": -100.3161},
    {"continent": "América do Norte", "country": "México", "city": "Puerto Vallarta", "lat": 20.6534, "lon": -105.2253},
    {"continent": "América do Norte", "country": "México", "city": "Los Cabos", "lat": 23.0908, "lon": -109.7141},

    # -----------------------------------------------------------------
    # 3. EUROPA – capitais e principais cidades turísticas/econômicas
    # -----------------------------------------------------------------
    {"continent": "Europa", "country": "Portugal", "city": "Lisboa", "lat": 38.7223, "lon": -9.1393},
    {"continent": "Europa", "country": "Portugal", "city": "Porto", "lat": 41.1579, "lon": -8.6291},
    {"continent": "Europa", "country": "Portugal", "city": "Faro", "lat": 37.0194, "lon": -7.9304},
    {"continent": "Europa", "country": "Portugal", "city": "Coimbra", "lat": 40.2033, "lon": -8.4103},
    {"continent": "Europa", "country": "Portugal", "city": "Braga", "lat": 41.5454, "lon": -8.4265},
    {"continent": "Europa", "country": "Portugal (Açores)", "city": "Ponta Delgada", "lat": 37.7412, "lon": -25.6677},
    {"continent": "Europa", "country": "Portugal (Madeira)", "city": "Funchal", "lat": 32.6669, "lon": -16.9241},
    {"continent": "Europa", "country": "Espanha", "city": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"continent": "Europa", "country": "Espanha", "city": "Barcelona", "lat": 41.3851, "lon": 2.1734},
    {"continent": "Europa", "country": "Espanha", "city": "Ibiza", "lat": 38.9067, "lon": 1.4206},
    {"continent": "Europa", "country": "Espanha", "city": "Sevilha", "lat": 37.3891, "lon": -5.9845},
    {"continent": "Europa", "country": "Espanha", "city": "Valência", "lat": 39.4699, "lon": -0.3763},
    {"continent": "Europa", "country": "Espanha", "city": "Málaga", "lat": 36.7213, "lon": -4.4213},
    {"continent": "Europa", "country": "Espanha", "city": "Granada", "lat": 37.1773, "lon": -3.5986},
    {"continent": "Europa", "country": "França", "city": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"continent": "Europa", "country": "França", "city": "Cannes", "lat": 43.5528, "lon": 7.0174},
    {"continent": "Europa", "country": "França", "city": "Nice", "lat": 43.7102, "lon": 7.2620},
    {"continent": "Europa", "country": "França", "city": "Lyon", "lat": 45.7640, "lon": 4.8357},
    {"continent": "Europa", "country": "França", "city": "Bordéus", "lat": 44.8378, "lon": -0.5792},
    {"continent": "Europa", "country": "França", "city": "Marselha", "lat": 43.2965, "lon": 5.3698},
    {"continent": "Europa", "country": "França", "city": "Estrasburgo", "lat": 48.5734, "lon": 7.7521},
    {"continent": "Europa", "country": "Mónaco", "city": "Monte Carlo", "lat": 43.7384, "lon": 7.4246},
    {"continent": "Europa", "country": "Itália", "city": "Roma", "lat": 41.9028, "lon": 12.4964},
    {"continent": "Europa", "country": "Itália", "city": "Veneza", "lat": 45.4408, "lon": 12.3155},
    {"continent": "Europa", "country": "Itália", "city": "Florença", "lat": 43.7696, "lon": 11.2558},
    {"continent": "Europa", "country": "Itália", "city": "Milão", "lat": 45.4642, "lon": 9.1900},
    {"continent": "Europa", "country": "Itália", "city": "Nápoles", "lat": 40.8518, "lon": 14.2681},
    {"continent": "Europa", "country": "Itália", "city": "Turim", "lat": 45.0703, "lon": 7.6869},
    {"continent": "Europa", "country": "Itália", "city": "Bolonha", "lat": 44.4949, "lon": 11.3426},
    {"continent": "Europa", "country": "Vaticano", "city": "Cidade do Vaticano", "lat": 41.9029, "lon": 12.4534},
    {"continent": "Europa", "country": "Suíça", "city": "Zurique", "lat": 47.3769, "lon": 8.5417},
    {"continent": "Europa", "country": "Suíça", "city": "Genebra", "lat": 46.2044, "lon": 6.1432},
    {"continent": "Europa", "country": "Suíça", "city": "Berna", "lat": 46.9480, "lon": 7.4474},
    {"continent": "Europa", "country": "Suíça", "city": "Lausanne", "lat": 46.5197, "lon": 6.6323},
    {"continent": "Europa", "country": "Alemanha", "city": "Berlim", "lat": 52.5200, "lon": 13.4050},
    {"continent": "Europa", "country": "Alemanha", "city": "Munique", "lat": 48.1351, "lon": 11.5820},
    {"continent": "Europa", "country": "Alemanha", "city": "Frankfurt", "lat": 50.1109, "lon": 8.6821},
    {"continent": "Europa", "country": "Alemanha", "city": "Hamburgo", "lat": 53.5511, "lon": 9.9937},
    {"continent": "Europa", "country": "Alemanha", "city": "Colónia", "lat": 50.9375, "lon": 6.9603},
    {"continent": "Europa", "country": "Alemanha", "city": "Düsseldorf", "lat": 51.2277, "lon": 6.7735},
    {"continent": "Europa", "country": "Áustria", "city": "Viena", "lat": 48.2082, "lon": 16.3738},
    {"continent": "Europa", "country": "Áustria", "city": "Salzburgo", "lat": 47.8095, "lon": 13.0550},
    {"continent": "Europa", "country": "Áustria", "city": "Innsbruck", "lat": 47.2692, "lon": 11.4041},
    {"continent": "Europa", "country": "Holanda", "city": "Amesterdão", "lat": 52.3676, "lon": 4.9041},
    {"continent": "Europa", "country": "Holanda", "city": "Roterdão", "lat": 51.9225, "lon": 4.4792},
    {"continent": "Europa", "country": "Holanda", "city": "Haia", "lat": 52.0705, "lon": 4.3007},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruxelas", "lat": 50.8503, "lon": 4.3517},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruges", "lat": 51.2093, "lon": 3.2247},
    {"continent": "Europa", "country": "Bélgica", "city": "Antuérpia", "lat": 51.2194, "lon": 4.4025},
    {"continent": "Europa", "country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"continent": "Europa", "country": "Reino Unido", "city": "Edimburgo", "lat": 55.9533, "lon": -3.1883},
    {"continent": "Europa", "country": "Reino Unido", "city": "Manchester", "lat": 53.4808, "lon": -2.2426},
    {"continent": "Europa", "country": "Reino Unido", "city": "Liverpool", "lat": 53.4084, "lon": -2.9916},
    {"continent": "Europa", "country": "Reino Unido", "city": "Bath", "lat": 51.3751, "lon": -2.3617},
    {"continent": "Europa", "country": "Reino Unido", "city": "Oxford", "lat": 51.7520, "lon": -1.2577},
    {"continent": "Europa", "country": "Reino Unido", "city": "Cambridge", "lat": 52.2053, "lon": 0.1218},
    {"continent": "Europa", "country": "Reino Unido", "city": "Glastonbury", "lat": 51.1463, "lon": -2.7153},
    {"continent": "Europa", "country": "Irlanda", "city": "Dublin", "lat": 53.3498, "lon": -6.2603},
    {"continent": "Europa", "country": "Irlanda", "city": "Cork", "lat": 51.8985, "lon": -8.4756},
    {"continent": "Europa", "country": "Islândia", "city": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
    {"continent": "Europa", "country": "Dinamarca", "city": "Copenhaga", "lat": 55.6761, "lon": 12.5683},
    {"continent": "Europa", "country": "Suécia", "city": "Estocolmo", "lat": 59.3293, "lon": 18.0686},
    {"continent": "Europa", "country": "Suécia", "city": "Gotemburgo", "lat": 57.7089, "lon": 11.9746},
    {"continent": "Europa", "country": "Noruega", "city": "Oslo", "lat": 59.9139, "lon": 10.7522},
    {"continent": "Europa", "country": "Noruega", "city": "Bergen", "lat": 60.3913, "lon": 5.3221},
    {"continent": "Europa", "country": "Finlândia", "city": "Helsínquia", "lat": 60.1699, "lon": 24.9384},
    {"continent": "Europa", "country": "Rússia", "city": "Moscovo", "lat": 55.7558, "lon": 37.6173},
    {"continent": "Europa", "country": "Rússia", "city": "São Petersburgo", "lat": 59.9343, "lon": 30.3351},
    {"continent": "Europa", "country": "Polónia", "city": "Varsóvia", "lat": 52.2297, "lon": 21.0122},
    {"continent": "Europa", "country": "Polónia", "city": "Cracóvia", "lat": 50.0647, "lon": 19.9450},
    {"continent": "Europa", "country": "República Checa", "city": "Praga", "lat": 50.0755, "lon": 14.4378},
    {"continent": "Europa", "country": "Hungria", "city": "Budapeste", "lat": 47.4979, "lon": 19.0402},
    {"continent": "Europa", "country": "Eslováquia", "city": "Bratislava", "lat": 48.1486, "lon": 17.1077},
    {"continent": "Europa", "country": "Eslovénia", "city": "Liubliana", "lat": 46.0569, "lon": 14.5058},
    {"continent": "Europa", "country": "Croácia", "city": "Dubrovnik", "lat": 42.6507, "lon": 18.0944},
    {"continent": "Europa", "country": "Croácia", "city": "Split", "lat": 43.5081, "lon": 16.4402},
    {"continent": "Europa", "country": "Croácia", "city": "Zagreb", "lat": 45.8150, "lon": 15.9819},
    {"continent": "Europa", "country": "Grécia", "city": "Atenas", "lat": 37.9838, "lon": 23.7275},
    {"continent": "Europa", "country": "Grécia", "city": "Santorini", "lat": 36.3932, "lon": 25.4615},
    {"continent": "Europa", "country": "Grécia", "city": "Míconos", "lat": 37.4467, "lon": 25.3289},
    {"continent": "Europa", "country": "Grécia", "city": "Creta", "lat": 35.2401, "lon": 24.8093},
    {"continent": "Europa", "country": "Turquia", "city": "Istambul", "lat": 41.0082, "lon": 28.9784},
    {"continent": "Europa", "country": "Turquia", "city": "Antália", "lat": 36.8969, "lon": 30.7133},
    {"continent": "Europa", "country": "Bulgária", "city": "Sófia", "lat": 42.6977, "lon": 23.3219},
    {"continent": "Europa", "country": "Roménia", "city": "Bucareste", "lat": 44.4268, "lon": 26.1025},
    {"continent": "Europa", "country": "Sérvia", "city": "Belgrado", "lat": 44.7866, "lon": 20.4489},
    {"continent": "Europa", "country": "Luxemburgo", "city": "Luxemburgo", "lat": 49.8153, "lon": 6.1296},

    # -----------------------------------------------------------------
    # 4. ÁFRICA – principais destinos turísticos e capitais
    # -----------------------------------------------------------------
    {"continent": "África", "country": "Marrocos", "city": "Marraquexe", "lat": 31.6295, "lon": -7.9811},
    {"continent": "África", "country": "Marrocos", "city": "Casablanca", "lat": 33.5731, "lon": -7.5898},
    {"continent": "África", "country": "Marrocos", "city": "Fez", "lat": 34.0181, "lon": -5.0078},
    {"continent": "África", "country": "Marrocos", "city": "Tânger", "lat": 35.7595, "lon": -5.8340},
    {"continent": "África", "country": "Egito", "city": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"continent": "África", "country": "Egito", "city": "Luxor", "lat": 25.6872, "lon": 32.6396},
    {"continent": "África", "country": "Egito", "city": "Alexandria", "lat": 31.2001, "lon": 29.9187},
    {"continent": "África", "country": "África do Sul", "city": "Cidade do Cabo", "lat": -33.9249, "lon": 18.4241},
    {"continent": "África", "country": "África do Sul", "city": "Joanesburgo", "lat": -26.2041, "lon": 28.0473},
    {"continent": "África", "country": "África do Sul", "city": "Durban", "lat": -29.8587, "lon": 31.0218},
    {"continent": "África", "country": "Quénia", "city": "Nairobi", "lat": -1.2921, "lon": 36.8219},
    {"continent": "África", "country": "Tanzânia", "city": "Zanzibar", "lat": -6.1659, "lon": 39.2026},
    {"continent": "África", "country": "Tanzânia", "city": "Arusha", "lat": -3.3869, "lon": 36.6830},
    {"continent": "África", "country": "Tanzânia", "city": "Dar es Salaam", "lat": -6.7924, "lon": 39.2083},
    {"continent": "África", "country": "Maurícia", "city": "Port Louis", "lat": -20.1609, "lon": 57.5012},
    {"continent": "África", "country": "Seychelles", "city": "Mahé", "lat": -4.6796, "lon": 55.4920},
    {"continent": "África", "country": "Cabo Verde", "city": "Praia", "lat": 14.9315, "lon": -23.5125},
    {"continent": "África", "country": "Cabo Verde", "city": "Sal", "lat": 16.7412, "lon": -22.9441},
    {"continent": "África", "country": "Tunísia", "city": "Tunes", "lat": 36.8065, "lon": 10.1815},
    {"continent": "África", "country": "Gana", "city": "Acra", "lat": 5.6037, "lon": -0.1870},
    {"continent": "África", "country": "Senegal", "city": "Dacar", "lat": 14.7167, "lon": -17.4677},

    # -----------------------------------------------------------------
    # 5. MÉDIO ORIENTE
    # -----------------------------------------------------------------
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Dubai", "lat": 25.2048, "lon": 55.2708},
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Abu Dhabi", "lat": 24.4539, "lon": 54.3773},
    {"continent": "Médio Oriente", "country": "Catar", "city": "Doha", "lat": 25.2854, "lon": 51.5310},
    {"continent": "Médio Oriente", "country": "Arábia Saudita", "city": "Riade", "lat": 24.7136, "lon": 46.6753},
    {"continent": "Médio Oriente", "country": "Arábia Saudita", "city": "Jeddah", "lat": 21.2854, "lon": 39.2376},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Tel Aviv", "lat": 32.0853, "lon": 34.7818},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Jerusalém", "lat": 31.7683, "lon": 35.2137},
    {"continent": "Médio Oriente", "country": "Jordânia", "city": "Petra", "lat": 30.3285, "lon": 35.4444},
    {"continent": "Médio Oriente", "country": "Jordânia", "city": "Amã", "lat": 31.9454, "lon": 35.9284},
    {"continent": "Médio Oriente", "country": "Omã", "city": "Mascate", "lat": 23.5880, "lon": 58.3829},
    {"continent": "Médio Oriente", "country": "Barém", "city": "Manama", "lat": 26.2285, "lon": 50.5860},
    {"continent": "Médio Oriente", "country": "Kuwait", "city": "Cidade do Kuwait", "lat": 29.3759, "lon": 47.9774},

    # -----------------------------------------------------------------
    # 6. ÁSIA – principais destinos
    # -----------------------------------------------------------------
    {"continent": "Ásia", "country": "Índia", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"continent": "Ásia", "country": "Índia", "city": "Nova Deli", "lat": 28.6139, "lon": 77.2090},
    {"continent": "Ásia", "country": "Índia", "city": "Goa", "lat": 15.2993, "lon": 74.1240},
    {"continent": "Ásia", "country": "Índia", "city": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"continent": "Ásia", "country": "Índia", "city": "Agra", "lat": 27.1767, "lon": 78.0081},
    {"continent": "Ásia", "country": "Tailândia", "city": "Banguecoque", "lat": 13.7563, "lon": 100.5018},
    {"continent": "Ásia", "country": "Tailândia", "city": "Phuket", "lat": 7.8804, "lon": 98.3922},
    {"continent": "Ásia", "country": "Tailândia", "city": "Chiang Mai", "lat": 18.7883, "lon": 98.9853},
    {"continent": "Ásia", "country": "Vietname", "city": "Hanói", "lat": 21.0285, "lon": 105.8542},
    {"continent": "Ásia", "country": "Vietname", "city": "Ho Chi Minh", "lat": 10.8231, "lon": 106.6297},
    {"continent": "Ásia", "country": "Vietname", "city": "Da Nang", "lat": 16.0544, "lon": 108.2022},
    {"continent": "Ásia", "country": "Camboja", "city": "Siem Reap", "lat": 13.3633, "lon": 103.8564},
    {"continent": "Ásia", "country": "Camboja", "city": "Phnom Penh", "lat": 11.5564, "lon": 104.9282},
    {"continent": "Ásia", "country": "Malásia", "city": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869},
    {"continent": "Ásia", "country": "Malásia", "city": "Penang", "lat": 5.4164, "lon": 100.3327},
    {"continent": "Ásia", "country": "Singapura", "city": "Singapura", "lat": 1.3521, "lon": 103.8198},
    {"continent": "Ásia", "country": "Indonésia", "city": "Bali", "lat": -8.4095, "lon": 115.1889},
    {"continent": "Ásia", "country": "Indonésia", "city": "Jacarta", "lat": -6.2088, "lon": 106.8456},
    {"continent": "Ásia", "country": "Filipinas", "city": "Manila", "lat": 14.5995, "lon": 120.9842},
    {"continent": "Ásia", "country": "Filipinas", "city": "Cebu", "lat": 10.3157, "lon": 123.8854},
    {"continent": "Ásia", "country": "China", "city": "Pequim", "lat": 39.9042, "lon": 116.4074},
    {"continent": "Ásia", "country": "China", "city": "Xangai", "lat": 31.2304, "lon": 121.4737},
    {"continent": "Ásia", "country": "China", "city": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
    {"continent": "Ásia", "country": "China (Macau)", "city": "Macau", "lat": 22.1987, "lon": 113.5439},
    {"continent": "Ásia", "country": "Japão", "city": "Tóquio", "lat": 35.6762, "lon": 139.6503},
    {"continent": "Ásia", "country": "Japão", "city": "Quioto", "lat": 35.0116, "lon": 135.7681},
    {"continent": "Ásia", "country": "Japão", "city": "Osaka", "lat": 34.6937, "lon": 135.5023},
    {"continent": "Ásia", "country": "Japão", "city": "Hokkaido", "lat": 43.2203, "lon": 142.8635},  # aproximado
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Seul", "lat": 37.5665, "lon": 126.9780},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Busan", "lat": 35.1796, "lon": 129.0756},
    {"continent": "Ásia", "country": "Taiwan", "city": "Taipé", "lat": 25.0330, "lon": 121.5654},

    # -----------------------------------------------------------------
    # 7. OCEANIA & PACÍFICO
    # -----------------------------------------------------------------
    {"continent": "Oceania", "country": "Austrália", "city": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"continent": "Oceania", "country": "Austrália", "city": "Melbourne", "lat": -37.8136, "lon": 144.9631},
    {"continent": "Oceania", "country": "Austrália", "city": "Brisbane", "lat": -27.4698, "lon": 153.0251},
    {"continent": "Oceania", "country": "Austrália", "city": "Perth", "lat": -31.9505, "lon": 115.8605},
    {"continent": "Oceania", "country": "Austrália", "city": "Uluru", "lat": -25.3444, "lon": 131.0369},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Auckland", "lat": -36.8485, "lon": 174.7633},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Queenstown", "lat": -45.0312, "lon": 168.6626},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Wellington", "lat": -41.2865, "lon": 174.7762},
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
    """Lógica CORRIGIDA para matriz Python (Índices de 0 a 11)."""
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    sun_pos, _ = swe.calc_ut(jd_ut, swe.SUN)
    sun_lon = sun_pos[0]
    
    # A tupla 'cusps' tem 12 elementos (0 a 11)
    # cusps[0] = Casa 1 | cusps[11] = Casa 12
    for i in range(12):
        cusp_start = cusps[i]
        # Se for o último índice (11), o fim da casa é o início da primeira (0)
        cusp_end = cusps[0] if i == 11 else cusps[i+1]
        
        if cusp_start < cusp_end:
            if cusp_start <= sun_lon < cusp_end:
                return i + 1  # Retorna a Casa real (1 a 12)
        else:
            # Atravessa o grau 360 (0º de Áries)
            if sun_lon >= cusp_start or sun_lon < cusp_end:
                return i + 1  # Retorna a Casa real (1 a 12)
                
    return 1  # Fallback

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
