import swisseph as swe
from datetime import datetime, timedelta
import os
import requests
import google.generativeai as genai
import pytz
from timezonefinder import TimezoneFinder
import logging
from collections import Counter

# ========== CONFIGURAÇÃO GERAL ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

swe.set_ephe_path('/usr/share/sweph/ephe')
tz_finder = TimezoneFinder()

# ========== ARQUÉTIPOS DAS CASAS ==========
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

# ========== BANCO DE DADOS PREMIUM COMPLETO ==========
PREMIUM_CITIES = [
    # 1. BRASIL
    {"continent": "América do Sul", "country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333, "tags": ["carreira", "negócios", "fama", "dinheiro", "networking"], "score": 8},
    {"continent": "América do Sul", "country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "tags": ["lazer", "criatividade", "praia", "fama", "diversão"], "score": 8},
    {"continent": "América do Sul", "country": "Brasil", "city": "Salvador", "lat": -12.9714, "lon": -38.5014, "tags": ["cultura", "festa", "espiritualidade", "história"], "score": 7},
    {"continent": "América do Sul", "country": "Brasil", "city": "Florianópolis", "lat": -27.5954, "lon": -48.5480, "tags": ["natureza", "bem-estar", "praia", "tecnologia", "inovação"], "score": 7},
    {"continent": "América do Sul", "country": "Brasil", "city": "Foz do Iguaçu", "lat": -25.5478, "lon": -54.5882, "tags": ["natureza", "energia", "turismo"], "score": 7},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fernando de Noronha", "lat": -3.8403, "lon": -32.4297, "tags": ["natureza", "luxo", "exclusividade", "romance", "isolamento"], "score": 7},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fortaleza", "lat": -3.7172, "lon": -38.5433, "tags": ["praia", "lazer", "diversão", "festa"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Natal", "lat": -5.7793, "lon": -35.2009, "tags": ["praia", "natureza", "paz"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Recife", "lat": -8.0476, "lon": -34.8770, "tags": ["cultura", "tecnologia", "história", "negócios"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Maceió", "lat": -9.6659, "lon": -35.7350, "tags": ["praia", "lazer", "romance"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Brasília", "lat": -15.7975, "lon": -47.8919, "tags": ["poder", "autoridade", "arquitetura", "networking"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345, "tags": ["cultura", "negócios", "gastronomia"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Curitiba", "lat": -25.4296, "lon": -49.2719, "tags": ["organização", "inovação", "trabalho", "frio"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Balneário Camboriú", "lat": -26.9917, "lon": -48.6333, "tags": ["luxo", "dinheiro", "festa", "praia", "fama"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "Búzios", "lat": -22.7478, "lon": -41.8819, "tags": ["luxo", "romance", "praia", "exclusividade"], "score": 6},
    {"continent": "América do Sul", "country": "Brasil", "city": "João Pessoa", "lat": -7.1150, "lon": -34.8610, "tags": ["paz", "tranquilidade", "praia", "família"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Aracaju", "lat": -10.9472, "lon": -37.0731, "tags": ["tranquilidade", "família", "praia"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Vitória", "lat": -20.3155, "lon": -40.3128, "tags": ["negócios", "praia", "tranquilidade"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Alegre", "lat": -30.0346, "lon": -51.2177, "tags": ["cultura", "negócios", "frio"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Seguro", "lat": -16.4435, "lon": -39.0643, "tags": ["história", "festa", "praia", "lazer"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Angra dos Reis", "lat": -23.0067, "lon": -44.3185, "tags": ["luxo", "natureza", "isolamento", "mar"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Paraty", "lat": -23.2192, "lon": -44.7153, "tags": ["história", "cultura", "arte", "romance"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ilhabela", "lat": -23.7785, "lon": -45.3552, "tags": ["natureza", "luxo", "isolamento"], "score": 5},
    {"continent": "América do Sul", "country": "Brasil", "city": "Manaus", "lat": -3.1190, "lon": -60.0217, "tags": ["natureza", "aventura", "retiro", "cura"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Belém", "lat": -1.4558, "lon": -48.5039, "tags": ["cultura", "história", "natureza"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Luís", "lat": -2.5297, "lon": -44.3028, "tags": ["história", "cultura", "praia"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Goiânia", "lat": -16.6864, "lon": -49.2643, "tags": ["negócios", "música", "dinheiro"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Santos", "lat": -23.9535, "lon": -46.3350, "tags": ["negócios", "praia", "história"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Blumenau", "lat": -26.9185, "lon": -49.0659, "tags": ["cultura", "festa", "organização"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Itajaí", "lat": -26.9081, "lon": -48.6707, "tags": ["negócios", "dinheiro", "praia"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ilhéus", "lat": -14.7939, "lon": -39.0460, "tags": ["história", "praia", "romance"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Cabo Frio", "lat": -22.8794, "lon": -42.0192, "tags": ["praia", "tranquilidade", "família"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ubatuba", "lat": -23.4372, "lon": -45.0700, "tags": ["natureza", "aventura", "praia"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Guarujá", "lat": -23.9935, "lon": -46.2567, "tags": ["praia", "imóveis", "família"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Sebastião", "lat": -23.8027, "lon": -45.4042, "tags": ["praia", "juventude", "agitação"], "score": 4},
    {"continent": "América do Sul", "country": "Brasil", "city": "Cuiabá", "lat": -15.6010, "lon": -56.0974, "tags": ["natureza", "negócios"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Campo Grande", "lat": -20.4697, "lon": -54.6201, "tags": ["natureza", "tranquilidade"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Juazeiro do Norte", "lat": -7.2133, "lon": -39.3151, "tags": ["espiritualidade", "fé", "cultura"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Campina Grande", "lat": -7.2219, "lon": -35.8739, "tags": ["tecnologia", "festa", "cultura"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Caruaru", "lat": -8.2835, "lon": -35.9698, "tags": ["cultura", "comércio", "vendas"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Bertioga", "lat": -23.8546, "lon": -46.1383, "tags": ["natureza", "família", "paz"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Caraguatatuba", "lat": -23.6203, "lon": -45.4131, "tags": ["praia", "família", "comércio"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Corumbá", "lat": -19.0097, "lon": -57.6514, "tags": ["natureza", "isolamento", "aventura"], "score": 3},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Velho", "lat": -8.7608, "lon": -63.8999, "tags": ["natureza", "isolamento"], "score": 2},
    {"continent": "América do Sul", "country": "Brasil", "city": "Teresina", "lat": -5.0892, "lon": -42.8019, "tags": ["negócios", "calor"], "score": 2},

    # 2. AMÉRICA DO SUL (EXCETO BRASIL)
    {"continent": "América do Sul", "country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816, "tags": ["cultura", "arte", "romance", "gastronomia"], "score": 8},
    {"continent": "América do Sul", "country": "Argentina", "city": "Mendoza", "lat": -32.8895, "lon": -68.8458, "tags": ["romance", "luxo", "natureza", "gastronomia"], "score": 6},
    {"continent": "América do Sul", "country": "Argentina", "city": "Bariloche", "lat": -41.1335, "lon": -71.3103, "tags": ["natureza", "aventura", "frio", "romance"], "score": 6},
    {"continent": "América do Sul", "country": "Argentina", "city": "Córdoba", "lat": -31.4201, "lon": -64.1888, "tags": ["estudos", "juventude", "cultura"], "score": 5},
    {"continent": "América do Sul", "country": "Chile", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "tags": ["negócios", "montanhas", "estabilidade"], "score": 6},
    {"continent": "América do Sul", "country": "Chile", "city": "Valparaíso", "lat": -33.0456, "lon": -71.6197, "tags": ["arte", "cultura", "criatividade"], "score": 5},
    {"continent": "América do Sul", "country": "Uruguai", "city": "Punta del Este", "lat": -34.9667, "lon": -54.9500, "tags": ["luxo", "dinheiro", "status", "praia", "festa"], "score": 6},
    {"continent": "América do Sul", "country": "Uruguai", "city": "Montevidéu", "lat": -34.9011, "lon": -56.1645, "tags": ["paz", "tranquilidade", "cultura"], "score": 5},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Bogotá", "lat": 4.7110, "lon": -74.0721, "tags": ["negócios", "história", "frio"], "score": 6},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Medellín", "lat": 6.2442, "lon": -75.5812, "tags": ["romance", "criatividade", "lazer", "inovação"], "score": 6},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Cartagena", "lat": 10.3910, "lon": -75.4794, "tags": ["história", "romance", "calor", "praia"], "score": 6},
    {"continent": "América do Sul", "country": "Peru", "city": "Lima", "lat": -12.0464, "lon": -77.0428, "tags": ["gastronomia", "história", "cultura"], "score": 6},
    {"continent": "América do Sul", "country": "Peru", "city": "Cusco", "lat": -13.5226, "lon": -71.9673, "tags": ["espiritualidade", "história", "misticismo", "transformação"], "score": 7},
    {"continent": "América do Sul", "country": "Equador", "city": "Quito", "lat": -0.1807, "lon": -78.4678, "tags": ["história", "natureza", "altitude"], "score": 5},
    {"continent": "América do Sul", "country": "Bolívia", "city": "La Paz", "lat": -16.4897, "lon": -68.1193, "tags": ["cultura", "isolamento", "misticismo"], "score": 4},
    {"continent": "América do Sul", "country": "Paraguai", "city": "Assunção", "lat": -25.2637, "lon": -57.5759, "tags": ["comércio", "vendas", "dinheiro"], "score": 3},
    {"continent": "América do Sul", "country": "Venezuela", "city": "Caracas", "lat": 10.4806, "lon": -66.9036, "tags": ["crise", "transformação", "intensidade"], "score": 2},

    # 3. AMÉRICA CENTRAL E CARIBE
    {"continent": "América Central", "country": "República Dominicana", "city": "Punta Cana", "lat": 18.5820, "lon": -68.4055, "tags": ["lazer", "romance", "praia", "diversão"], "score": 7},
    {"continent": "América Central", "country": "Panamá", "city": "Cidade do Panamá", "lat": 8.9824, "lon": -79.5199, "tags": ["negócios", "comércio", "dinheiro", "metrópole"], "score": 6},
    {"continent": "América Central", "country": "Cuba", "city": "Havana", "lat": 23.1136, "lon": -82.3666, "tags": ["história", "arte", "música", "passado"], "score": 6},
    {"continent": "América Central", "country": "Porto Rico", "city": "San Juan", "lat": 18.4655, "lon": -66.1057, "tags": ["festa", "cultura", "música"], "score": 6},
    {"continent": "América Central", "country": "Bahamas", "city": "Nassau", "lat": 25.0443, "lon": -77.3504, "tags": ["luxo", "praia", "lazer", "dinheiro"], "score": 6},
    {"continent": "América Central", "country": "Costa Rica", "city": "San José", "lat": 9.9281, "lon": -84.0907, "tags": ["natureza", "bem-estar", "saúde", "paz"], "score": 5},
    {"continent": "América Central", "country": "República Dominicana", "city": "Santo Domingo", "lat": 18.4861, "lon": -69.9312, "tags": ["história", "praia"], "score": 5},
    {"continent": "América Central", "country": "Guatemala", "city": "Cidade da Guatemala", "lat": 14.6349, "lon": -90.5069, "tags": ["história", "cultura"], "score": 4},

    # 4. AMÉRICA DO NORTE
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Iorque", "lat": 40.7128, "lon": -74.0060, "tags": ["carreira", "negócios", "fama", "dinheiro", "metrópole"], "score": 10},
    {"continent": "América do Norte", "country": "EUA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "tags": ["fama", "criatividade", "cinema", "status", "arte"], "score": 9},
    {"continent": "América do Norte", "country": "EUA", "city": "Chicago", "lat": 41.8781, "lon": -87.6298, "tags": ["negócios", "arquitetura", "trabalho"], "score": 8},
    {"continent": "América do Norte", "country": "EUA", "city": "Miami", "lat": 25.7617, "lon": -80.1918, "tags": ["festa", "praia", "luxo", "diversão", "dinheiro"], "score": 8},
    {"continent": "América do Norte", "country": "EUA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398, "tags": ["sorte", "diversão", "entretenimento", "dinheiro"], "score": 8},
    {"continent": "América do Norte", "country": "EUA", "city": "São Francisco", "lat": 37.7749, "lon": -122.4194, "tags": ["inovação", "tecnologia", "futuro", "networking"], "score": 8},
    {"continent": "América do Norte", "country": "Canadá", "city": "Toronto", "lat": 43.6510, "lon": -79.3470, "tags": ["negócios", "dinheiro", "metrópole", "trabalho"], "score": 8},
    {"continent": "América do Norte", "country": "Canadá", "city": "Vancouver", "lat": 49.2827, "lon": -123.1207, "tags": ["natureza", "bem-estar", "saúde", "qualidade de vida"], "score": 8},
    {"continent": "América do Norte", "country": "México", "city": "Cidade do México", "lat": 19.4326, "lon": -99.1332, "tags": ["cultura", "metrópole", "história", "negócios"], "score": 8},
    {"continent": "América do Norte", "country": "EUA", "city": "Boston", "lat": 42.3601, "lon": -71.0589, "tags": ["estudos", "conhecimento", "história", "educação"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Washington D.C.", "lat": 38.9072, "lon": -77.0369, "tags": ["poder", "autoridade", "política", "liderança"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Seattle", "lat": 47.6062, "lon": -122.3321, "tags": ["tecnologia", "chuva", "natureza", "trabalho"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Orleans", "lat": 29.9511, "lon": -90.0715, "tags": ["música", "cultura", "misticismo", "festa"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Orlando", "lat": 28.5383, "lon": -81.3792, "tags": ["família", "diversão", "lazer", "entretenimento"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "San Diego", "lat": 32.7157, "lon": -117.1611, "tags": ["praia", "paz", "qualidade de vida", "saúde"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Nashville", "lat": 36.1627, "lon": -86.7816, "tags": ["música", "arte", "cultura", "entretenimento"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Aspen", "lat": 39.1911, "lon": -106.8175, "tags": ["luxo", "status", "frio", "esporte", "natureza"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Sedona", "lat": 34.8697, "lon": -111.7610, "tags": ["espiritualidade", "cura", "misticismo", "natureza", "retiro"], "score": 7},
    {"continent": "América do Norte", "country": "Canadá", "city": "Montreal", "lat": 45.5017, "lon": -73.5673, "tags": ["cultura", "arte", "estudos", "romance"], "score": 7},
    {"continent": "América do Norte", "country": "México", "city": "Cancún", "lat": 21.1619, "lon": -86.8515, "tags": ["lazer", "praia", "festa", "diversão", "sorte"], "score": 7},
    {"continent": "América do Norte", "country": "México", "city": "Tulum", "lat": 20.2114, "lon": -87.4654, "tags": ["espiritualidade", "cura", "natureza", "misticismo", "praia"], "score": 7},
    {"continent": "América do Norte", "country": "México", "city": "Los Cabos", "lat": 23.0908, "lon": -109.7141, "tags": ["luxo", "praia", "exclusividade", "dinheiro"], "score": 7},
    {"continent": "América do Norte", "country": "EUA", "city": "Denver", "lat": 39.7392, "lon": -104.9903, "tags": ["natureza", "aventura", "esporte", "montanhas"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Atlanta", "lat": 33.7490, "lon": -84.3880, "tags": ["negócios", "networking", "comunicação"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Dallas", "lat": 32.7767, "lon": -96.7970, "tags": ["dinheiro", "negócios", "poder"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Houston", "lat": 29.7604, "lon": -95.3698, "tags": ["tecnologia", "indústria", "trabalho"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Filadélfia", "lat": 39.9526, "lon": -75.1652, "tags": ["história", "raízes", "cultura"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Portland", "lat": 45.5051, "lon": -122.6750, "tags": ["natureza", "criatividade", "arte"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Charleston", "lat": 32.7765, "lon": -79.9311, "tags": ["história", "romance", "arquitetura"], "score": 6},
    {"continent": "América do Norte", "country": "Canadá", "city": "Calgary", "lat": 51.0447, "lon": -114.0719, "tags": ["indústria", "dinheiro", "trabalho"], "score": 6},
    {"continent": "América do Norte", "country": "Canadá", "city": "Québec", "lat": 46.8139, "lon": -71.2080, "tags": ["história", "frio", "cultura"], "score": 6},
    {"continent": "América do Norte", "country": "México", "city": "Guadalajara", "lat": 20.6597, "lon": -103.3496, "tags": ["cultura", "música", "tecnologia"], "score": 6},
    {"continent": "América do Norte", "country": "México", "city": "Puerto Vallarta", "lat": 20.6534, "lon": -105.2253, "tags": ["praia", "romance", "lazer"], "score": 6},
    {"continent": "América do Norte", "country": "EUA", "city": "Phoenix", "lat": 33.4484, "lon": -112.0740, "tags": ["calor", "isolamento", "cura"], "score": 5},
    {"continent": "América do Norte", "country": "EUA", "city": "Minneapolis", "lat": 44.9778, "lon": -93.2650, "tags": ["trabalho", "frio", "organização"], "score": 5},
    {"continent": "América do Norte", "country": "EUA", "city": "Memphis", "lat": 35.1495, "lon": -90.0490, "tags": ["música", "história"], "score": 5},
    {"continent": "América do Norte", "country": "EUA", "city": "Savannah", "lat": 32.0809, "lon": -81.0912, "tags": ["história", "mistério", "misticismo"], "score": 5},
    {"continent": "América do Norte", "country": "Canadá", "city": "Ottawa", "lat": 45.4215, "lon": -75.6972, "tags": ["poder", "política", "ordem"], "score": 5},
    {"continent": "América do Norte", "country": "México", "city": "Monterrey", "lat": 25.6866, "lon": -100.3161, "tags": ["indústria", "dinheiro", "negócios"], "score": 5},
    {"continent": "América do Norte", "country": "EUA", "city": "Detroit", "lat": 42.3314, "lon": -83.0458, "tags": ["renascimento", "indústria", "transformação"], "score": 4},
    {"continent": "América do Norte", "country": "EUA", "city": "St. Louis", "lat": 38.6270, "lon": -90.1994, "tags": ["história", "comércio"], "score": 4},
    {"continent": "América do Norte", "country": "EUA", "city": "Kansas City", "lat": 39.0997, "lon": -94.5786, "tags": ["raízes", "estabilidade"], "score": 4},

    # 5. EUROPA
    {"continent": "Europa", "country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lon": -0.1278, "tags": ["fama", "poder", "negócios", "história", "dinheiro", "status"], "score": 10},
    {"continent": "Europa", "country": "França", "city": "Paris", "lat": 48.8566, "lon": 2.3522, "tags": ["romance", "arte", "beleza", "fama", "moda", "luxo"], "score": 10},
    {"continent": "Europa", "country": "Itália", "city": "Roma", "lat": 41.9028, "lon": 12.4964, "tags": ["história", "poder", "antiguidade", "religião", "arquitetura"], "score": 10},
    {"continent": "Europa", "country": "Espanha", "city": "Madrid", "lat": 40.4168, "lon": -3.7038, "tags": ["cultura", "arte", "negócios", "metrópole"], "score": 9},
    {"continent": "Europa", "country": "Espanha", "city": "Barcelona", "lat": 41.3851, "lon": 2.1734, "tags": ["criatividade", "arte", "praia", "arquitetura", "lazer"], "score": 9},
    {"continent": "Europa", "country": "Itália", "city": "Milão", "lat": 45.4642, "lon": 9.1900, "tags": ["moda", "negócios", "design", "luxo", "dinheiro"], "score": 9},
    {"continent": "Europa", "country": "Alemanha", "city": "Berlim", "lat": 52.5200, "lon": 13.4050, "tags": ["transformação", "história", "criatividade", "vanguarda", "renascimento"], "score": 9},
    {"continent": "Europa", "country": "Holanda", "city": "Amesterdão", "lat": 52.3676, "lon": 4.9041, "tags": ["liberdade", "comércio", "inovação", "diversão", "tolerância"], "score": 9},
    {"continent": "Europa", "country": "Turquia", "city": "Istambul", "lat": 41.0082, "lon": 28.9784, "tags": ["cultura", "comércio", "mistério", "ponte", "história"], "score": 9},
    {"continent": "Europa", "country": "Portugal", "city": "Lisboa", "lat": 38.7223, "lon": -9.1393, "tags": ["luz", "história", "romance", "criatividade", "comunicação"], "score": 8},
    {"continent": "Europa", "country": "Portugal", "city": "Porto", "lat": 41.1579, "lon": -8.6291, "tags": ["trabalho", "tradição", "negócios", "raízes"], "score": 7},
    {"continent": "Europa", "country": "Portugal (Madeira)", "city": "Funchal", "lat": 32.6669, "lon": -16.9241, "tags": ["natureza", "beleza", "tranquilidade", "lazer"], "score": 7},
    {"continent": "Europa", "country": "Portugal (Açores)", "city": "Ponta Delgada", "lat": 37.7412, "lon": -25.6677, "tags": ["natureza", "isolamento", "paz", "cura", "retiro"], "score": 5},
    {"continent": "Europa", "country": "Suíça", "city": "Zurique", "lat": 47.3769, "lon": 8.5417, "tags": ["dinheiro", "finanças", "segurança", "bancos", "ordem", "luxo"], "score": 8},
    {"continent": "Europa", "country": "Suíça", "city": "Genebra", "lat": 46.2044, "lon": 6.1432, "tags": ["diplomacia", "paz", "alianças", "dinheiro"], "score": 7},
    {"continent": "Europa", "country": "Itália", "city": "Veneza", "lat": 45.4408, "lon": 12.3155, "tags": ["romance", "beleza", "água", "mistério", "arte"], "score": 8},
    {"continent": "Europa", "country": "Itália", "city": "Florença", "lat": 43.7696, "lon": 11.2558, "tags": ["arte", "criatividade", "beleza", "história", "renascimento"], "score": 8},
    {"continent": "Europa", "country": "Dinamarca", "city": "Copenhaga", "lat": 55.6761, "lon": 12.5683, "tags": ["design", "bem-estar", "sociedade", "ordem", "inovação"], "score": 8},
    {"continent": "Europa", "country": "Áustria", "city": "Viena", "lat": 48.2082, "lon": 16.3738, "tags": ["cultura", "arte", "música", "arquitetura", "psicologia"], "score": 8},
    {"continent": "Europa", "country": "Áustria", "city": "Innsbruck", "lat": 47.2692, "lon": 11.4041, "tags": ["esporte", "aventura", "natureza"], "score": 5},
    {"continent": "Europa", "country": "Alemanha", "city": "Munique", "lat": 48.1351, "lon": 11.5820, "tags": ["dinheiro", "tecnologia", "tradição", "ordem"], "score": 8},
    {"continent": "Europa", "country": "Alemanha", "city": "Frankfurt", "lat": 50.1109, "lon": 8.6821, "tags": ["finanças", "negócios", "bancos", "dinheiro", "poder"], "score": 7},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruxelas", "lat": 50.8503, "lon": 4.3517, "tags": ["diplomacia", "poder", "alianças", "organização"], "score": 7},
    {"continent": "Europa", "country": "Reino Unido", "city": "Edimburgo", "lat": 55.9533, "lon": -3.1883, "tags": ["mistério", "história", "literatura", "arte"], "score": 7},
    {"continent": "Europa", "country": "Irlanda", "city": "Dublin", "lat": 53.3498, "lon": -6.2603, "tags": ["literatura", "tecnologia", "comunicação", "networking"], "score": 7},
    {"continent": "Europa", "country": "Suécia", "city": "Estocolmo", "lat": 59.3293, "lon": 18.0686, "tags": ["tecnologia", "inovação", "design", "sociedade"], "score": 7},
    {"continent": "Europa", "country": "Noruega", "city": "Oslo", "lat": 59.9139, "lon": 10.7522, "tags": ["natureza", "paz", "riqueza", "organização"], "score": 7},
    {"continent": "Europa", "country": "República Checa", "city": "Praga", "lat": 50.0755, "lon": 14.4378, "tags": ["arquitetura", "mistério", "magia", "romance", "história"], "score": 7},
    {"continent": "Europa", "country": "Hungria", "city": "Budapeste", "lat": 47.4979, "lon": 19.0402, "tags": ["beleza", "águas termais", "saúde", "história"], "score": 7},
    {"continent": "Europa", "country": "Croácia", "city": "Dubrovnik", "lat": 42.6507, "lon": 18.0944, "tags": ["história", "mar", "beleza", "status"], "score": 7},
    {"continent": "Europa", "country": "Grécia", "city": "Atenas", "lat": 37.9838, "lon": 23.7275, "tags": ["filosofia", "sabedoria", "história", "raízes", "estudos"], "score": 7},
    {"continent": "Europa", "country": "Grécia", "city": "Santorini", "lat": 36.3932, "lon": 25.4615, "tags": ["romance", "beleza", "luxo", "casamento"], "score": 8},
    {"continent": "Europa", "country": "Mónaco", "city": "Monte Carlo", "lat": 43.7384, "lon": 7.4246, "tags": ["luxo", "dinheiro", "riqueza", "status", "exclusividade"], "score": 8},
    {"continent": "Europa", "country": "Vaticano", "city": "Cidade do Vaticano", "lat": 41.9029, "lon": 12.4534, "tags": ["espiritualidade", "poder", "fé", "segredo", "religião"], "score": 8},
    {"continent": "Europa", "country": "Espanha", "city": "Ibiza", "lat": 38.9067, "lon": 1.4206, "tags": ["festa", "diversão", "liberdade", "praia"], "score": 7},
    {"continent": "Europa", "country": "França", "city": "Cannes", "lat": 43.5528, "lon": 7.0174, "tags": ["fama", "luxo", "cinema", "status", "glamour"], "score": 7},
    {"continent": "Europa", "country": "França", "city": "Nice", "lat": 43.7102, "lon": 7.2620, "tags": ["beleza", "praia", "descanso", "luxo"], "score": 7},

    # 6. ÁFRICA
    {"continent": "África", "country": "Marrocos", "city": "Marraquexe", "lat": 31.6295, "lon": -7.9811, "tags": ["cores", "comércio", "misticismo", "exotismo"], "score": 8},
    {"continent": "África", "country": "Egito", "city": "Cairo", "lat": 30.0444, "lon": 31.2357, "tags": ["antiguidade", "história", "mistério", "raízes"], "score": 8},
    {"continent": "África", "country": "África do Sul", "city": "Cidade do Cabo", "lat": -33.9249, "lon": 18.4241, "tags": ["natureza", "beleza", "aventura", "vinho", "turismo"], "score": 8},
    {"continent": "África", "country": "Tanzânia", "city": "Zanzibar", "lat": -6.1659, "lon": 39.2026, "tags": ["praia", "exotismo", "romance", "especiarias"], "score": 7},
    {"continent": "África", "country": "Seychelles", "city": "Mahé", "lat": -4.6796, "lon": 55.4920, "tags": ["luxo", "exclusividade", "natureza", "romance", "casamento"], "score": 6},

    # 7. MÉDIO ORIENTE
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Dubai", "lat": 25.2048, "lon": 55.2708, "tags": ["dinheiro", "luxo", "comércio", "fama", "futuro", "negócios"], "score": 10},
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Abu Dhabi", "lat": 24.4539, "lon": 54.3773, "tags": ["riqueza", "poder", "petróleo", "cultura", "luxo"], "score": 8},
    {"continent": "Médio Oriente", "country": "Catar", "city": "Doha", "lat": 25.2854, "lon": 51.5310, "tags": ["dinheiro", "arquitetura", "futuro", "esporte"], "score": 7},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Jerusalém", "lat": 31.7683, "lon": 35.2137, "tags": ["espiritualidade", "religião", "história", "fé", "conflito"], "score": 7},

    # 8. ÁSIA
    {"continent": "Ásia", "country": "Tailândia", "city": "Banguecoque", "lat": 13.7563, "lon": 100.5018, "tags": ["comércio", "diversão", "templos", "gastronomia"], "score": 10},
    {"continent": "Ásia", "country": "Singapura", "city": "Singapura", "lat": 1.3521, "lon": 103.8198, "tags": ["tecnologia", "dinheiro", "ordem", "limpeza", "finanças", "futuro"], "score": 10},
    {"continent": "Ásia", "country": "Indonésia", "city": "Bali", "lat": -8.4095, "lon": 115.1889, "tags": ["espiritualidade", "cura", "natureza", "romance", "retiro", "bem-estar"], "score": 10},
    {"continent": "Ásia", "country": "Japão", "city": "Tóquio", "lat": 35.6762, "lon": 139.6503, "tags": ["tecnologia", "ordem", "trabalho", "futuro", "metrópole", "eficiência"], "score": 10},
    {"continent": "Ásia", "country": "Malásia", "city": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869, "tags": ["modernidade", "negócios", "compras", "mistura"], "score": 9},
    {"continent": "Ásia", "country": "China", "city": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "tags": ["dinheiro", "comércio", "finanças", "tecnologia", "densidade"], "score": 9},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Seul", "lat": 37.5665, "lon": 126.9780, "tags": ["tecnologia", "beleza", "moda", "inovação", "dinheiro", "cultura pop"], "score": 9},
    {"continent": "Ásia", "country": "China", "city": "Pequim", "lat": 39.9042, "lon": 116.4074, "tags": ["poder", "história", "política", "autoridade", "tradição"], "score": 8},
    {"continent": "Ásia", "country": "China", "city": "Xangai", "lat": 31.2304, "lon": 121.4737, "tags": ["negócios", "finanças", "dinheiro", "futuro", "metrópole"], "score": 8},
    {"continent": "Ásia", "country": "Japão", "city": "Quioto", "lat": 35.0116, "lon": 135.7681, "tags": ["tradição", "espiritualidade", "templos", "paz", "cultura", "beleza"], "score": 8},
    {"continent": "Ásia", "country": "Índia", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "tags": ["fama", "cinema", "negócios", "multidão", "intensidade"], "score": 7},
    {"continent": "Ásia", "country": "Índia", "city": "Nova Deli", "lat": 28.6139, "lon": 77.2090, "tags": ["poder", "política", "história", "caos", "transformação"], "score": 7},

    # 9. OCEANIA
    {"continent": "Oceania", "country": "Austrália", "city": "Sydney", "lat": -33.8688, "lon": 151.2093, "tags": ["praia", "ação", "negócios", "beleza", "esporte", "lazer"], "score": 9},
    {"continent": "Oceania", "country": "Austrália", "city": "Melbourne", "lat": -37.8136, "lon": 144.9631, "tags": ["arte", "cultura", "cafés", "criatividade"], "score": 8},
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Bora Bora", "lat": -16.5004, "lon": -151.7415, "tags": ["luxo", "romance", "lua de mel", "exclusividade", "praia"], "score": 8},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Auckland", "lat": -36.8485, "lon": 174.7633, "tags": ["mar", "vela", "natureza", "comércio"], "score": 7},
    {"continent": "Oceania", "country": "Havaí", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583, "tags": ["praia", "surf", "natureza", "espírito aloha", "férias", "lazer"], "score": 7},
]

# ========== NORMALIZAÇÃO DE NOMES ==========
def normalize_city_name(city, country=None):
    if not city:
        return None
    city = city.strip()
    aliases = {
        "new york city": "New York",
        "nyc": "New York",
        "sao paulo": "São Paulo",
        "rio de janeiro": "Rio de Janeiro",
        "london": "London",
        "los angeles": "Los Angeles",
        "buenos aires": "Buenos Aires",
        "bangkok": "Banguecoque"
    }
    city_lower = city.lower()
    city = aliases.get(city_lower, city.title())
    if country:
        return f"{city}, {country}"
    return city

# ========== NOVA BUSCA EXCLUSIVA NO BANCO PREMIUM ==========
def search_premium_cities(query, country=None):
    query_lower = query.strip().lower()
    matches = []
    for c in PREMIUM_CITIES:
        city_lower = c['city'].lower()
        country_lower = c['country'].lower()
        if city_lower == query_lower or query_lower in city_lower or city_lower in query_lower:
            if country is not None:
                if country_lower == country.lower():
                    matches.append(c)
            else:
                matches.append(c)
    return matches

# ========== BUSCA GLOBAL (RESTORED) ==========
def get_natal_coordinates(city_name, country=None):
    """Busca qualquer cidade no mundo via API global para garantir que cidades como Surubim funcionem."""
    query = f"{city_name}, {country}" if country else city_name
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    headers = {'User-Agent': 'HouseScannerApp/1.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200 and resp.json():
            data = resp.json()[0]
            return {
                "lat": float(data["lat"]),
                "lon": float(data["lon"])
            }
    except Exception as e:
        logger.error(f"Erro na busca global para {query}: {e}")
    raise ValueError(f"Não foi possível localizar as coordenadas para: {query}")

# ========== GEOCODING SEGURO ==========
def get_canonical_coordinates(city_name, country=None):
    """Tenta o banco Premium; se não achar (ex: Surubim), usa a busca global."""
    matches = search_premium_cities(city_name, country)
    if matches:
        c = matches[0]
        return {
            "lat": c['lat'],
            "lon": c['lon'],
            "city": c['city'],
            "country": c['country'],
            "display_name": normalize_city_name(c['city'], c['country'])
        }
    
    # Fallback para busca global se não estiver no premium
    coords = get_natal_coordinates(city_name, country)
    return {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "city": city_name,
        "country": country,
        "display_name": normalize_city_name(city_name, country)
    }

# ========== FUSO HORÁRIO (TRAVADO CONTRA ERRO DE UTC) ==========
def get_timezone(lat, lon):
    tz_name = tz_finder.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        tz_name = tz_finder.certain_timezone_at(lat=lat, lng=lon)
    if not tz_name:
        raise ValueError(f"Fuso horário não pôde ser determinado para coordenadas ({lat}, {lon}).")
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

# ========== FUNÇÕES DE DATA ==========
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

def get_stable_house(city_lat, city_lon, jd_return, natal_cusps):
    offsets = [-0.15, 0, 0.15]
    houses = []
    for dlat in offsets:
        for dlon in offsets:
            lat = city_lat + dlat
            lon = city_lon + dlon
            _, ascmc = swe.houses_ex(jd_return, lat, lon, b'P')
            sr_ascendant = ascmc[0]
            house = get_house_superposition(sr_ascendant, natal_cusps)
            houses.append(house)
    counter = Counter(houses)
    return counter.most_common(1)[0][0]

def compute_solar_return_data(natal_data, target_year):
    birth_local = parse_birth_datetime(natal_data['dob'], natal_data['time'])
    natal_lat = natal_data.get('natal_lat')
    natal_lon = natal_data.get('natal_lon')
    
    if natal_lat is None or natal_lon is None:
        coords = get_natal_coordinates(natal_data['place_of_birth'], natal_data.get('birth_country'))
        natal_lat, natal_lon = coords["lat"], coords["lon"]
        
    natal_lat = float(natal_lat)
    natal_lon = float(natal_lon)
    
    birth_utc = local_to_utc(natal_lat, natal_lon, birth_local)
    jd_natal = swe.julday(birth_utc.year, birth_utc.month, birth_utc.day, birth_utc.hour + birth_utc.minute / 60.0)
    jd_return = calculate_solar_return(jd_natal, int(target_year), birth_local.month, birth_local.day)
    natal_cusps, _ = swe.houses_ex(jd_natal, natal_lat, natal_lon, b'P')
    
    return jd_return, natal_cusps

def get_house_for_city(city_lat, city_lon, natal_data, target_year):
    jd_return, natal_cusps = compute_solar_return_data(natal_data, target_year)
    return get_stable_house(city_lat, city_lon, jd_return, natal_cusps)

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
    base_score = city.get("score", 0)
    city_tags = city.get("tags", [])
    archetype_tags = HOUSE_ARCHETYPES.get(house_id, [])
    match_archetype = len(set(city_tags) & set(archetype_tags))
    match_intent = 0
    if user_intent:
        intent_lower = user_intent.lower()
        for tag in city_tags:
            if tag in intent_lower:
                match_intent += 1
        for word in archetype_tags:
            if word in intent_lower:
                match_intent += 0.5
    tier = get_city_tier(city)
    tier_bonus = 2 if tier == "highticket" else (1 if tier == "acessivel" else 0)
    total = base_score + (match_archetype * 3) + (match_intent * 4) + tier_bonus
    if match_intent >= 3:
        total += 8
    elif match_intent >= 2:
        total += 5
    return total

def scan_premium_houses(jd_return, natal_cusps, user_intent=""):
    results = {i: {"city": None, "lat": None, "lon": None, "longitude": None, "options": {"highticket": [], "acessivel": [], "nacional": []}} for i in range(1, 13)}
    valid_cities_per_house = {i: [] for i in range(1, 13)}
    for city in PREMIUM_CITIES:
        house = get_stable_house(city["lat"], city["lon"], jd_return, natal_cusps)
        total_score = score_city_for_house(city, house, user_intent)
        display_name = normalize_city_name(city["city"], city["country"])
        city_data = {"city": city["city"], "country": city["country"], "continent": city["continent"], "display_name": display_name, "lat": city["lat"], "lon": city["lon"], "tier": get_city_tier(city), "score": total_score, "tags": city.get("tags", [])}
        valid_cities_per_house[house].append(city_data)
    for i in range(1, 13):
        if valid_cities_per_house[i]:
            valid_cities_per_house[i].sort(key=lambda x: x["score"], reverse=True)
            best_city = valid_cities_per_house[i][0]
            results[i]["city"] = best_city
            results[i]["lat"] = best_city["lat"]
            results[i]["lon"] = best_city["lon"]
            results[i]["longitude"] = best_city["lon"]
            tier_groups = {"highticket": [], "acessivel": [], "nacional": []}
            for city in valid_cities_per_house[i]:
                tier_groups[city["tier"]].append(city)
            for tier in tier_groups:
                tier_groups[tier].sort(key=lambda x: x["score"], reverse=True)
                if tier_groups[tier]:
                    results[i]["options"][tier] = tier_groups[tier][:3]
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
