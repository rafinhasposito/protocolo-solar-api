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

# Certifique-se de que este caminho está correto no seu servidor
swe.set_ephe_path('/usr/share/sweph/ephe')

# Carrega o buscador de fuso horário em memória global para altíssima performance
tz_finder = TimezoneFinder()

# ========== ARQUÉTIPOS DAS CASAS (SISTEMA DE SCORING) ==========
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

# ========== BANCO DE DADOS PREMIUM TAGUEADO (120+ CIDADES) ==========
PREMIUM_CITIES = [
    # 1. BRASIL
    {"continent": "América do Sul", "country": "Brasil", "city": "Manaus", "lat": -3.1190, "lon": -60.0217, "tags": ["natureza", "aventura", "retiro", "cura"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Belém", "lat": -1.4558, "lon": -48.5039, "tags": ["cultura", "história", "natureza"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Velho", "lat": -8.7608, "lon": -63.8999, "tags": ["natureza", "isolamento"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Luís", "lat": -2.5297, "lon": -44.3028, "tags": ["história", "cultura", "praia"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Teresina", "lat": -5.0892, "lon": -42.8019, "tags": ["negócios", "calor"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fortaleza", "lat": -3.7172, "lon": -38.5433, "tags": ["praia", "lazer", "diversão", "festa"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Natal", "lat": -5.7793, "lon": -35.2009, "tags": ["praia", "natureza", "paz"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "João Pessoa", "lat": -7.1150, "lon": -34.8610, "tags": ["paz", "tranquilidade", "praia", "família"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Recife", "lat": -8.0476, "lon": -34.8770, "tags": ["cultura", "tecnologia", "história", "negócios"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Maceió", "lat": -9.6659, "lon": -35.7350, "tags": ["praia", "lazer", "romance"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Aracaju", "lat": -10.9472, "lon": -37.0731, "tags": ["tranquilidade", "família", "praia"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Salvador", "lat": -12.9714, "lon": -38.5014, "tags": ["cultura", "festa", "espiritualidade", "história"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Cuiabá", "lat": -15.6010, "lon": -56.0974, "tags": ["natureza", "negócios"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Campo Grande", "lat": -20.4697, "lon": -54.6201, "tags": ["natureza", "tranquilidade"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Goiânia", "lat": -16.6864, "lon": -49.2643, "tags": ["negócios", "música", "dinheiro"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Brasília", "lat": -15.7975, "lon": -47.8919, "tags": ["poder", "autoridade", "arquitetura", "networking"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345, "tags": ["cultura", "negócios", "gastronomia"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Vitória", "lat": -20.3155, "lon": -40.3128, "tags": ["negócios", "praia", "tranquilidade"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "tags": ["lazer", "criatividade", "praia", "fama", "diversão"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lon": -46.6333, "tags": ["carreira", "negócios", "fama", "dinheiro", "networking"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Curitiba", "lat": -25.4296, "lon": -49.2719, "tags": ["organização", "inovação", "trabalho", "frio"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Florianópolis", "lat": -27.5954, "lon": -48.5480, "tags": ["natureza", "bem-estar", "praia", "tecnologia", "inovação"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Alegre", "lat": -30.0346, "lon": -51.2177, "tags": ["cultura", "negócios", "frio"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Santos", "lat": -23.9535, "lon": -46.3350, "tags": ["negócios", "praia", "história"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Blumenau", "lat": -26.9185, "lon": -49.0659, "tags": ["cultura", "festa", "organização"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Itajaí", "lat": -26.9081, "lon": -48.6707, "tags": ["negócios", "dinheiro", "praia"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Balneário Camboriú", "lat": -26.9917, "lon": -48.6333, "tags": ["luxo", "dinheiro", "festa", "praia", "fama"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Foz do Iguaçu", "lat": -25.5478, "lon": -54.5882, "tags": ["natureza", "energia", "turismo"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Juazeiro do Norte", "lat": -7.2133, "lon": -39.3151, "tags": ["espiritualidade", "fé", "cultura"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Campina Grande", "lat": -7.2219, "lon": -35.8739, "tags": ["tecnologia", "festa", "cultura"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Caruaru", "lat": -8.2835, "lon": -35.9698, "tags": ["cultura", "comércio", "vendas"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ilhéus", "lat": -14.7939, "lon": -39.0460, "tags": ["história", "praia", "romance"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Porto Seguro", "lat": -16.4435, "lon": -39.0643, "tags": ["história", "festa", "praia", "lazer"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Cabo Frio", "lat": -22.8794, "lon": -42.0192, "tags": ["praia", "tranquilidade", "família"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Búzios", "lat": -22.7478, "lon": -41.8819, "tags": ["luxo", "romance", "praia", "exclusividade"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Angra dos Reis", "lat": -23.0067, "lon": -44.3185, "tags": ["luxo", "natureza", "isolamento", "mar"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Paraty", "lat": -23.2192, "lon": -44.7153, "tags": ["história", "cultura", "arte", "romance"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ubatuba", "lat": -23.4372, "lon": -45.0700, "tags": ["natureza", "aventura", "praia"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Ilhabela", "lat": -23.7785, "lon": -45.3552, "tags": ["natureza", "luxo", "isolamento"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Guarujá", "lat": -23.9935, "lon": -46.2567, "tags": ["praia", "imóveis", "família"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Bertioga", "lat": -23.8546, "lon": -46.1383, "tags": ["natureza", "família", "paz"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "São Sebastião", "lat": -23.8027, "lon": -45.4042, "tags": ["praia", "juventude", "agitação"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Caraguatatuba", "lat": -23.6203, "lon": -45.4131, "tags": ["praia", "família", "comércio"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Corumbá", "lat": -19.0097, "lon": -57.6514, "tags": ["natureza", "isolamento", "aventura"]},
    {"continent": "América do Sul", "country": "Brasil", "city": "Fernando de Noronha", "lat": -3.8403, "lon": -32.4297, "tags": ["natureza", "luxo", "exclusividade", "romance", "isolamento"]},

    # 1.5. AMÉRICA DO SUL (RESTANTE) E AMÉRICA CENTRAL
    {"continent": "América do Sul", "country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816, "tags": ["cultura", "arte", "romance", "gastronomia"]},
    {"continent": "América do Sul", "country": "Argentina", "city": "Córdoba", "lat": -31.4201, "lon": -64.1888, "tags": ["estudos", "juventude", "cultura"]},
    {"continent": "América do Sul", "country": "Argentina", "city": "Mendoza", "lat": -32.8895, "lon": -68.8458, "tags": ["romance", "luxo", "natureza", "gastronomia"]},
    {"continent": "América do Sul", "country": "Argentina", "city": "Bariloche", "lat": -41.1335, "lon": -71.3103, "tags": ["natureza", "aventura", "frio", "romance"]},
    {"continent": "América do Sul", "country": "Chile", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "tags": ["negócios", "montanhas", "estabilidade"]},
    {"continent": "América do Sul", "country": "Chile", "city": "Valparaíso", "lat": -33.0456, "lon": -71.6197, "tags": ["arte", "cultura", "criatividade"]},
    {"continent": "América do Sul", "country": "Uruguai", "city": "Montevidéu", "lat": -34.9011, "lon": -56.1645, "tags": ["paz", "tranquilidade", "cultura"]},
    {"continent": "América do Sul", "country": "Uruguai", "city": "Punta del Este", "lat": -34.9667, "lon": -54.9500, "tags": ["luxo", "dinheiro", "status", "praia", "festa"]},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Bogotá", "lat": 4.7110, "lon": -74.0721, "tags": ["negócios", "história", "frio"]},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Medellín", "lat": 6.2442, "lon": -75.5812, "tags": ["romance", "criatividade", "lazer", "inovação"]},
    {"continent": "América do Sul", "country": "Colômbia", "city": "Cartagena", "lat": 10.3910, "lon": -75.4794, "tags": ["história", "romance", "calor", "praia"]},
    {"continent": "América do Sul", "country": "Peru", "city": "Lima", "lat": -12.0464, "lon": -77.0428, "tags": ["gastronomia", "história", "cultura"]},
    {"continent": "América do Sul", "country": "Peru", "city": "Cusco", "lat": -13.5226, "lon": -71.9673, "tags": ["espiritualidade", "história", "misticismo", "transformação"]},
    {"continent": "América do Sul", "country": "Equador", "city": "Quito", "lat": -0.1807, "lon": -78.4678, "tags": ["história", "natureza", "altitude"]},
    {"continent": "América do Sul", "country": "Bolívia", "city": "La Paz", "lat": -16.4897, "lon": -68.1193, "tags": ["cultura", "isolamento", "misticismo"]},
    {"continent": "América do Sul", "country": "Paraguai", "city": "Assunção", "lat": -25.2637, "lon": -57.5759, "tags": ["comércio", "vendas", "dinheiro"]},
    {"continent": "América do Sul", "country": "Venezuela", "city": "Caracas", "lat": 10.4806, "lon": -66.9036, "tags": ["crise", "transformação", "intensidade"]},
    {"continent": "América Central", "country": "Panamá", "city": "Cidade do Panamá", "lat": 8.9824, "lon": -79.5199, "tags": ["negócios", "comércio", "dinheiro", "metrópole"]},
    {"continent": "América Central", "country": "Costa Rica", "city": "San José", "lat": 9.9281, "lon": -84.0907, "tags": ["natureza", "bem-estar", "saúde", "paz"]},
    {"continent": "América Central", "country": "Guatemala", "city": "Cidade da Guatemala", "lat": 14.6349, "lon": -90.5069, "tags": ["história", "cultura"]},
    {"continent": "América Central", "country": "República Dominicana", "city": "Santo Domingo", "lat": 18.4861, "lon": -69.9312, "tags": ["história", "praia"]},
    {"continent": "América Central", "country": "República Dominicana", "city": "Punta Cana", "lat": 18.5820, "lon": -68.4055, "tags": ["lazer", "romance", "praia", "diversão"]},
    {"continent": "América Central", "country": "Cuba", "city": "Havana", "lat": 23.1136, "lon": -82.3666, "tags": ["história", "arte", "música", "passado"]},
    {"continent": "América Central", "country": "Porto Rico", "city": "San Juan", "lat": 18.4655, "lon": -66.1057, "tags": ["festa", "cultura", "música"]},
    {"continent": "América Central", "country": "Bahamas", "city": "Nassau", "lat": 25.0443, "lon": -77.3504, "tags": ["luxo", "praia", "lazer", "dinheiro"]},

    # 2. AMÉRICA DO NORTE
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Iorque", "lat": 40.7128, "lon": -74.0060, "tags": ["carreira", "negócios", "fama", "dinheiro", "metrópole"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "tags": ["fama", "criatividade", "cinema", "status", "arte"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Chicago", "lat": 41.8781, "lon": -87.6298, "tags": ["negócios", "arquitetura", "trabalho"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Miami", "lat": 25.7617, "lon": -80.1918, "tags": ["festa", "praia", "luxo", "diversão", "dinheiro"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398, "tags": ["sorte", "diversão", "entretenimento", "dinheiro"]},
    {"continent": "América do Norte", "country": "EUA", "city": "São Francisco", "lat": 37.7749, "lon": -122.4194, "tags": ["inovação", "tecnologia", "futuro", "networking"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Boston", "lat": 42.3601, "lon": -71.0589, "tags": ["estudos", "conhecimento", "história", "educação"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Washington D.C.", "lat": 38.9072, "lon": -77.0369, "tags": ["poder", "autoridade", "política", "liderança"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Seattle", "lat": 47.6062, "lon": -122.3321, "tags": ["tecnologia", "chuva", "natureza", "trabalho"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Denver", "lat": 39.7392, "lon": -104.9903, "tags": ["natureza", "aventura", "esporte", "montanhas"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Nova Orleans", "lat": 29.9511, "lon": -90.0715, "tags": ["música", "cultura", "misticismo", "festa"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Orlando", "lat": 28.5383, "lon": -81.3792, "tags": ["família", "diversão", "lazer", "entretenimento"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Atlanta", "lat": 33.7490, "lon": -84.3880, "tags": ["negócios", "networking", "comunicação"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Dallas", "lat": 32.7767, "lon": -96.7970, "tags": ["dinheiro", "negócios", "poder"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Houston", "lat": 29.7604, "lon": -95.3698, "tags": ["tecnologia", "indústria", "trabalho"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Filadélfia", "lat": 39.9526, "lon": -75.1652, "tags": ["história", "raízes", "cultura"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Phoenix", "lat": 33.4484, "lon": -112.0740, "tags": ["calor", "isolamento", "cura"]},
    {"continent": "América do Norte", "country": "EUA", "city": "San Diego", "lat": 32.7157, "lon": -117.1611, "tags": ["praia", "paz", "qualidade de vida", "saúde"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Portland", "lat": 45.5051, "lon": -122.6750, "tags": ["natureza", "criatividade", "arte"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Detroit", "lat": 42.3314, "lon": -83.0458, "tags": ["renascimento", "indústria", "transformação"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Minneapolis", "lat": 44.9778, "lon": -93.2650, "tags": ["trabalho", "frio", "organização"]},
    {"continent": "América do Norte", "country": "EUA", "city": "St. Louis", "lat": 38.6270, "lon": -90.1994, "tags": ["história", "comércio"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Kansas City", "lat": 39.0997, "lon": -94.5786, "tags": ["raízes", "estabilidade"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Nashville", "lat": 36.1627, "lon": -86.7816, "tags": ["música", "arte", "cultura", "entretenimento"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Memphis", "lat": 35.1495, "lon": -90.0490, "tags": ["música", "história"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Charleston", "lat": 32.7765, "lon": -79.9311, "tags": ["história", "romance", "arquitetura"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Savannah", "lat": 32.0809, "lon": -81.0912, "tags": ["história", "mistério", "misticismo"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Aspen", "lat": 39.1911, "lon": -106.8175, "tags": ["luxo", "status", "frio", "esporte", "natureza"]},
    {"continent": "América do Norte", "country": "EUA", "city": "Sedona", "lat": 34.8697, "lon": -111.7610, "tags": ["espiritualidade", "cura", "misticismo", "natureza", "retiro"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Toronto", "lat": 43.6510, "lon": -79.3470, "tags": ["negócios", "dinheiro", "metrópole", "trabalho"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Vancouver", "lat": 49.2827, "lon": -123.1207, "tags": ["natureza", "bem-estar", "saúde", "qualidade de vida"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Montreal", "lat": 45.5017, "lon": -73.5673, "tags": ["cultura", "arte", "estudos", "romance"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Calgary", "lat": 51.0447, "lon": -114.0719, "tags": ["indústria", "dinheiro", "trabalho"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Ottawa", "lat": 45.4215, "lon": -75.6972, "tags": ["poder", "política", "ordem"]},
    {"continent": "América do Norte", "country": "Canadá", "city": "Québec", "lat": 46.8139, "lon": -71.2080, "tags": ["história", "frio", "cultura"]},
    {"continent": "América do Norte", "country": "México", "city": "Cidade do México", "lat": 19.4326, "lon": -99.1332, "tags": ["cultura", "metrópole", "história", "negócios"]},
    {"continent": "América do Norte", "country": "México", "city": "Cancún", "lat": 21.1619, "lon": -86.8515, "tags": ["lazer", "praia", "festa", "diversão", "sorte"]},
    {"continent": "América do Norte", "country": "México", "city": "Tulum", "lat": 20.2114, "lon": -87.4654, "tags": ["espiritualidade", "cura", "natureza", "misticismo", "praia"]},
    {"continent": "América do Norte", "country": "México", "city": "Guadalajara", "lat": 20.6597, "lon": -103.3496, "tags": ["cultura", "música", "tecnologia"]},
    {"continent": "América do Norte", "country": "México", "city": "Monterrey", "lat": 25.6866, "lon": -100.3161, "tags": ["indústria", "dinheiro", "negócios"]},
    {"continent": "América do Norte", "country": "México", "city": "Puerto Vallarta", "lat": 20.6534, "lon": -105.2253, "tags": ["praia", "romance", "lazer"]},
    {"continent": "América do Norte", "country": "México", "city": "Los Cabos", "lat": 23.0908, "lon": -109.7141, "tags": ["luxo", "praia", "exclusividade", "dinheiro"]},

    # 3. EUROPA
    {"continent": "Europa", "country": "Portugal", "city": "Lisboa", "lat": 38.7223, "lon": -9.1393, "tags": ["luz", "história", "romance", "criatividade", "comunicação"]},
    {"continent": "Europa", "country": "Portugal", "city": "Porto", "lat": 41.1579, "lon": -8.6291, "tags": ["trabalho", "tradição", "negócios", "raízes"]},
    {"continent": "Europa", "country": "Portugal", "city": "Faro", "lat": 37.0194, "lon": -7.9304, "tags": ["praia", "lazer", "férias"]},
    {"continent": "Europa", "country": "Portugal", "city": "Coimbra", "lat": 40.2033, "lon": -8.4103, "tags": ["estudos", "conhecimento", "juventude", "história"]},
    {"continent": "Europa", "country": "Portugal", "city": "Braga", "lat": 41.5454, "lon": -8.4265, "tags": ["religião", "paz", "tradição"]},
    {"continent": "Europa", "country": "Portugal (Açores)", "city": "Ponta Delgada", "lat": 37.7412, "lon": -25.6677, "tags": ["natureza", "isolamento", "paz", "cura", "retiro"]},
    {"continent": "Europa", "country": "Portugal (Madeira)", "city": "Funchal", "lat": 32.6669, "lon": -16.9241, "tags": ["natureza", "beleza", "tranquilidade", "lazer"]},
    {"continent": "Europa", "country": "Espanha", "city": "Madrid", "lat": 40.4168, "lon": -3.7038, "tags": ["cultura", "arte", "negócios", "metrópole"]},
    {"continent": "Europa", "country": "Espanha", "city": "Barcelona", "lat": 41.3851, "lon": 2.1734, "tags": ["criatividade", "arte", "praia", "arquitetura", "lazer"]},
    {"continent": "Europa", "country": "Espanha", "city": "Ibiza", "lat": 38.9067, "lon": 1.4206, "tags": ["festa", "diversão", "liberdade", "praia"]},
    {"continent": "Europa", "country": "Espanha", "city": "Sevilha", "lat": 37.3891, "lon": -5.9845, "tags": ["paixão", "cultura", "calor", "arte"]},
    {"continent": "Europa", "country": "Espanha", "city": "Valência", "lat": 39.4699, "lon": -0.3763, "tags": ["tecnologia", "praia", "inovação"]},
    {"continent": "Europa", "country": "Espanha", "city": "Málaga", "lat": 36.7213, "lon": -4.4213, "tags": ["arte", "história", "praia"]},
    {"continent": "Europa", "country": "Espanha", "city": "Granada", "lat": 37.1773, "lon": -3.5986, "tags": ["história", "misticismo", "arquitetura"]},
    {"continent": "Europa", "country": "França", "city": "Paris", "lat": 48.8566, "lon": 2.3522, "tags": ["romance", "arte", "beleza", "fama", "moda", "luxo"]},
    {"continent": "Europa", "country": "França", "city": "Cannes", "lat": 43.5528, "lon": 7.0174, "tags": ["fama", "luxo", "cinema", "status", "glamour"]},
    {"continent": "Europa", "country": "França", "city": "Nice", "lat": 43.7102, "lon": 7.2620, "tags": ["beleza", "praia", "descanso", "luxo"]},
    {"continent": "Europa", "country": "França", "city": "Lyon", "lat": 45.7640, "lon": 4.8357, "tags": ["gastronomia", "cultura", "tradição"]},
    {"continent": "Europa", "country": "França", "city": "Bordéus", "lat": 44.8378, "lon": -0.5792, "tags": ["tradição", "luxo", "raízes"]},
    {"continent": "Europa", "country": "França", "city": "Marselha", "lat": 43.2965, "lon": 5.3698, "tags": ["comércio", "diversidade", "mar"]},
    {"continent": "Europa", "country": "França", "city": "Estrasburgo", "lat": 48.5734, "lon": 7.7521, "tags": ["política", "diplomacia", "união", "alianças"]},
    {"continent": "Europa", "country": "Mónaco", "city": "Monte Carlo", "lat": 43.7384, "lon": 7.4246, "tags": ["luxo", "dinheiro", "riqueza", "status", "exclusividade"]},
    {"continent": "Europa", "country": "Itália", "city": "Roma", "lat": 41.9028, "lon": 12.4964, "tags": ["história", "poder", "antiguidade", "religião", "arquitetura"]},
    {"continent": "Europa", "country": "Itália", "city": "Veneza", "lat": 45.4408, "lon": 12.3155, "tags": ["romance", "beleza", "água", "mistério", "arte"]},
    {"continent": "Europa", "country": "Itália", "city": "Florença", "lat": 43.7696, "lon": 11.2558, "tags": ["arte", "criatividade", "beleza", "história", "renascimento"]},
    {"continent": "Europa", "country": "Itália", "city": "Milão", "lat": 45.4642, "lon": 9.1900, "tags": ["moda", "negócios", "design", "luxo", "dinheiro"]},
    {"continent": "Europa", "country": "Itália", "city": "Nápoles", "lat": 40.8518, "lon": 14.2681, "tags": ["paixão", "intensidade", "tradição"]},
    {"continent": "Europa", "country": "Itália", "city": "Turim", "lat": 45.0703, "lon": 7.6869, "tags": ["indústria", "mistério", "tecnologia"]},
    {"continent": "Europa", "country": "Itália", "city": "Bolonha", "lat": 44.4949, "lon": 11.3426, "tags": ["estudos", "conhecimento", "gastronomia"]},
    {"continent": "Europa", "country": "Vaticano", "city": "Cidade do Vaticano", "lat": 41.9029, "lon": 12.4534, "tags": ["espiritualidade", "poder", "fé", "segredo", "religião"]},
    {"continent": "Europa", "country": "Suíça", "city": "Zurique", "lat": 47.3769, "lon": 8.5417, "tags": ["dinheiro", "finanças", "segurança", "bancos", "ordem", "luxo"]},
    {"continent": "Europa", "country": "Suíça", "city": "Genebra", "lat": 46.2044, "lon": 6.1432, "tags": ["diplomacia", "paz", "alianças", "dinheiro"]},
    {"continent": "Europa", "country": "Suíça", "city": "Berna", "lat": 46.9480, "lon": 7.4474, "tags": ["política", "ordem", "poder"]},
    {"continent": "Europa", "country": "Suíça", "city": "Lausanne", "lat": 46.5197, "lon": 6.6323, "tags": ["esporte", "estudos", "natureza"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Berlim", "lat": 52.5200, "lon": 13.4050, "tags": ["transformação", "história", "criatividade", "vanguarda", "renascimento"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Munique", "lat": 48.1351, "lon": 11.5820, "tags": ["dinheiro", "tecnologia", "tradição", "ordem"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Frankfurt", "lat": 50.1109, "lon": 8.6821, "tags": ["finanças", "negócios", "bancos", "dinheiro", "poder"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Hamburgo", "lat": 53.5511, "lon": 9.9937, "tags": ["comércio", "indústria", "mar", "vendas"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Colónia", "lat": 50.9375, "lon": 6.9603, "tags": ["história", "religião", "comunicação"]},
    {"continent": "Europa", "country": "Alemanha", "city": "Düsseldorf", "lat": 51.2277, "lon": 6.7735, "tags": ["luxo", "moda", "negócios"]},
    {"continent": "Europa", "country": "Áustria", "city": "Viena", "lat": 48.2082, "lon": 16.3738, "tags": ["cultura", "arte", "música", "arquitetura", "psicologia"]},
    {"continent": "Europa", "country": "Áustria", "city": "Salzburgo", "lat": 47.8095, "lon": 13.0550, "tags": ["música", "arte", "natureza"]},
    {"continent": "Europa", "country": "Áustria", "city": "Innsbruck", "lat": 47.2692, "lon": 11.4041, "tags": ["esporte", "aventura", "natureza"]},
    {"continent": "Europa", "country": "Holanda", "city": "Amesterdão", "lat": 52.3676, "lon": 4.9041, "tags": ["liberdade", "comércio", "inovação", "diversão", "tolerância"]},
    {"continent": "Europa", "country": "Holanda", "city": "Roterdão", "lat": 51.9225, "lon": 4.4792, "tags": ["arquitetura", "comércio", "inovação"]},
    {"continent": "Europa", "country": "Holanda", "city": "Haia", "lat": 52.0705, "lon": 4.3007, "tags": ["justiça", "diplomacia", "ordem", "alianças"]},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruxelas", "lat": 50.8503, "lon": 4.3517, "tags": ["diplomacia", "poder", "alianças", "organização"]},
    {"continent": "Europa", "country": "Bélgica", "city": "Bruges", "lat": 51.2093, "lon": 3.2247, "tags": ["história", "romance", "beleza"]},
    {"continent": "Europa", "country": "Bélgica", "city": "Antuérpia", "lat": 51.2194, "lon": 4.4025, "tags": ["moda", "diamantes", "riqueza", "design"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lon": -0.1278, "tags": ["fama", "poder", "negócios", "história", "dinheiro", "status"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Edimburgo", "lat": 55.9533, "lon": -3.1883, "tags": ["mistério", "história", "literatura", "arte"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Manchester", "lat": 53.4808, "lon": -2.2426, "tags": ["indústria", "inovação", "esporte"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Liverpool", "lat": 53.4084, "lon": -2.9916, "tags": ["música", "arte", "mar"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Bath", "lat": 51.3751, "lon": -2.3617, "tags": ["saúde", "cura", "história", "romance"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Oxford", "lat": 51.7520, "lon": -1.2577, "tags": ["estudos", "conhecimento", "tradição", "filosofia"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Cambridge", "lat": 52.2053, "lon": 0.1218, "tags": ["estudos", "ciência", "inovação", "conhecimento"]},
    {"continent": "Europa", "country": "Reino Unido", "city": "Glastonbury", "lat": 51.1463, "lon": -2.7153, "tags": ["espiritualidade", "misticismo", "lendas", "magia", "cura"]},
    {"continent": "Europa", "country": "Irlanda", "city": "Dublin", "lat": 53.3498, "lon": -6.2603, "tags": ["literatura", "tecnologia", "comunicação", "networking"]},
    {"continent": "Europa", "country": "Irlanda", "city": "Cork", "lat": 51.8985, "lon": -8.4756, "tags": ["cultura", "tradição", "gastronomia"]},
    {"continent": "Europa", "country": "Islândia", "city": "Reykjavik", "lat": 64.1466, "lon": -21.9426, "tags": ["natureza", "isolamento", "frio", "energia", "cura", "transformação"]},
    {"continent": "Europa", "country": "Dinamarca", "city": "Copenhaga", "lat": 55.6761, "lon": 12.5683, "tags": ["design", "bem-estar", "sociedade", "ordem", "inovação"]},
    {"continent": "Europa", "country": "Suécia", "city": "Estocolmo", "lat": 59.3293, "lon": 18.0686, "tags": ["tecnologia", "inovação", "design", "sociedade"]},
    {"continent": "Europa", "country": "Suécia", "city": "Gotemburgo", "lat": 57.7089, "lon": 11.9746, "tags": ["sustentabilidade", "indústria", "natureza"]},
    {"continent": "Europa", "country": "Noruega", "city": "Oslo", "lat": 59.9139, "lon": 10.7522, "tags": ["natureza", "paz", "riqueza", "organização"]},
    {"continent": "Europa", "country": "Noruega", "city": "Bergen", "lat": 60.3913, "lon": 5.3221, "tags": ["natureza", "frio", "beleza"]},
    {"continent": "Europa", "country": "Finlândia", "city": "Helsínquia", "lat": 60.1699, "lon": 24.9384, "tags": ["educação", "tecnologia", "isolamento", "frio"]},
    {"continent": "Europa", "country": "Rússia", "city": "Moscovo", "lat": 55.7558, "lon": 37.6173, "tags": ["poder", "força", "autoridade", "transformação", "história"]},
    {"continent": "Europa", "country": "Rússia", "city": "São Petersburgo", "lat": 59.9343, "lon": 30.3351, "tags": ["arte", "cultura", "beleza", "literatura"]},
    {"continent": "Europa", "country": "Polónia", "city": "Varsóvia", "lat": 52.2297, "lon": 21.0122, "tags": ["renascimento", "história", "negócios"]},
    {"continent": "Europa", "country": "Polónia", "city": "Cracóvia", "lat": 50.0647, "lon": 19.9450, "tags": ["história", "tradição", "cultura"]},
    {"continent": "Europa", "country": "República Checa", "city": "Praga", "lat": 50.0755, "lon": 14.4378, "tags": ["arquitetura", "mistério", "magia", "romance", "história"]},
    {"continent": "Europa", "country": "Hungria", "city": "Budapeste", "lat": 47.4979, "lon": 19.0402, "tags": ["beleza", "águas termais", "saúde", "história"]},
    {"continent": "Europa", "country": "Eslováquia", "city": "Bratislava", "lat": 48.1486, "lon": 17.1077, "tags": ["tranquilidade", "rio", "história"]},
    {"continent": "Europa", "country": "Eslovénia", "city": "Liubliana", "lat": 46.0569, "lon": 14.5058, "tags": ["natureza", "sustentabilidade", "paz"]},
    {"continent": "Europa", "country": "Croácia", "city": "Dubrovnik", "lat": 42.6507, "lon": 18.0944, "tags": ["história", "mar", "beleza", "status"]},
    {"continent": "Europa", "country": "Croácia", "city": "Split", "lat": 43.5081, "lon": 16.4402, "tags": ["mar", "história", "verão"]},
    {"continent": "Europa", "country": "Croácia", "city": "Zagreb", "lat": 45.8150, "lon": 15.9819, "tags": ["cultura", "museus", "cafés"]},
    {"continent": "Europa", "country": "Grécia", "city": "Atenas", "lat": 37.9838, "lon": 23.7275, "tags": ["filosofia", "sabedoria", "história", "raízes", "estudos"]},
    {"continent": "Europa", "country": "Grécia", "city": "Santorini", "lat": 36.3932, "lon": 25.4615, "tags": ["romance", "beleza", "luxo", "casamento"]},
    {"continent": "Europa", "country": "Grécia", "city": "Míconos", "lat": 37.4467, "lon": 25.3289, "tags": ["festa", "diversão", "liberdade", "luxo"]},
    {"continent": "Europa", "country": "Grécia", "city": "Creta", "lat": 35.2401, "lon": 24.8093, "tags": ["mitologia", "história", "natureza"]},
    {"continent": "Europa", "country": "Turquia", "city": "Istambul", "lat": 41.0082, "lon": 28.9784, "tags": ["cultura", "comércio", "mistério", "ponte", "história"]},
    {"continent": "Europa", "country": "Turquia", "city": "Antália", "lat": 36.8969, "lon": 30.7133, "tags": ["mar", "descanso", "férias"]},
    {"continent": "Europa", "country": "Bulgária", "city": "Sófia", "lat": 42.6977, "lon": 23.3219, "tags": ["história", "religião", "tradição"]},
    {"continent": "Europa", "country": "Roménia", "city": "Bucareste", "lat": 44.4268, "lon": 26.1025, "tags": ["tecnologia", "contraste", "energia"]},
    {"continent": "Europa", "country": "Sérvia", "city": "Belgrado", "lat": 44.7866, "lon": 20.4489, "tags": ["vida noturna", "energia", "força"]},
    {"continent": "Europa", "country": "Luxemburgo", "city": "Luxemburgo", "lat": 49.8153, "lon": 6.1296, "tags": ["dinheiro", "finanças", "riqueza", "ordem"]},

    # 4. ÁFRICA
    {"continent": "África", "country": "Marrocos", "city": "Marraquexe", "lat": 31.6295, "lon": -7.9811, "tags": ["cores", "comércio", "misticismo", "exotismo"]},
    {"continent": "África", "country": "Marrocos", "city": "Casablanca", "lat": 33.5731, "lon": -7.5898, "tags": ["negócios", "romance", "mar"]},
    {"continent": "África", "country": "Marrocos", "city": "Fez", "lat": 34.0181, "lon": -5.0078, "tags": ["espiritualidade", "tradição", "história"]},
    {"continent": "África", "country": "Marrocos", "city": "Tânger", "lat": 35.7595, "lon": -5.8340, "tags": ["arte", "literatura", "encontros"]},
    {"continent": "África", "country": "Egito", "city": "Cairo", "lat": 30.0444, "lon": 31.2357, "tags": ["antiguidade", "história", "mistério", "raízes"]},
    {"continent": "África", "country": "Egito", "city": "Luxor", "lat": 25.6872, "lon": 32.6396, "tags": ["espiritualidade", "poder", "passado"]},
    {"continent": "África", "country": "Egito", "city": "Alexandria", "lat": 31.2001, "lon": 29.9187, "tags": ["conhecimento", "biblioteca", "mar"]},
    {"continent": "África", "country": "África do Sul", "city": "Cidade do Cabo", "lat": -33.9249, "lon": 18.4241, "tags": ["natureza", "beleza", "aventura", "vinho", "turismo"]},
    {"continent": "África", "country": "África do Sul", "city": "Joanesburgo", "lat": -26.2041, "lon": 28.0473, "tags": ["negócios", "riqueza", "ouro", "indústria"]},
    {"continent": "África", "country": "África do Sul", "city": "Durban", "lat": -29.8587, "lon": 31.0218, "tags": ["praia", "surf", "calor"]},
    {"continent": "África", "country": "Quénia", "city": "Nairobi", "lat": -1.2921, "lon": 36.8219, "tags": ["selvagem", "natureza", "tecnologia", "animais"]},
    {"continent": "África", "country": "Tanzânia", "city": "Zanzibar", "lat": -6.1659, "lon": 39.2026, "tags": ["praia", "exotismo", "romance", "especiarias"]},
    {"continent": "África", "country": "Tanzânia", "city": "Arusha", "lat": -3.3869, "lon": 36.6830, "tags": ["aventura", "safari", "montanha"]},
    {"continent": "África", "country": "Tanzânia", "city": "Dar es Salaam", "lat": -6.7924, "lon": 39.2083, "tags": ["comércio", "porto", "agitação"]},
    {"continent": "África", "country": "Maurícia", "city": "Port Louis", "lat": -20.1609, "lon": 57.5012, "tags": ["luxo", "praia", "romance", "isolamento"]},
    {"continent": "África", "country": "Seychelles", "city": "Mahé", "lat": -4.6796, "lon": 55.4920, "tags": ["luxo", "exclusividade", "natureza", "romance", "casamento"]},
    {"continent": "África", "country": "Cabo Verde", "city": "Praia", "lat": 14.9315, "lon": -23.5125, "tags": ["música", "mar", "cultura"]},
    {"continent": "África", "country": "Cabo Verde", "city": "Sal", "lat": 16.7412, "lon": -22.9441, "tags": ["sol", "praia", "descanso", "calor"]},
    {"continent": "África", "country": "Tunísia", "city": "Tunes", "lat": 36.8065, "lon": 10.1815, "tags": ["história", "mediterrâneo", "ruínas"]},
    {"continent": "África", "country": "Gana", "city": "Acra", "lat": 5.6037, "lon": -0.1870, "tags": ["energia", "crescimento", "cultura", "raízes"]},
    {"continent": "África", "country": "Senegal", "city": "Dacar", "lat": 14.7167, "lon": -17.4677, "tags": ["arte", "música", "oceano"]},

    # 5. MÉDIO ORIENTE
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Dubai", "lat": 25.2048, "lon": 55.2708, "tags": ["dinheiro", "luxo", "comércio", "fama", "futuro", "negócios"]},
    {"continent": "Médio Oriente", "country": "Emirados Árabes", "city": "Abu Dhabi", "lat": 24.4539, "lon": 54.3773, "tags": ["riqueza", "poder", "petróleo", "cultura", "luxo"]},
    {"continent": "Médio Oriente", "country": "Catar", "city": "Doha", "lat": 25.2854, "lon": 51.5310, "tags": ["dinheiro", "arquitetura", "futuro", "esporte"]},
    {"continent": "Médio Oriente", "country": "Arábia Saudita", "city": "Riade", "lat": 24.7136, "lon": 46.6753, "tags": ["negócios", "poder", "tradição"]},
    {"continent": "Médio Oriente", "country": "Arábia Saudita", "city": "Jeddah", "lat": 21.2854, "lon": 39.2376, "tags": ["mar vermelho", "comércio", "religião"]},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Tel Aviv", "lat": 32.0853, "lon": 34.7818, "tags": ["tecnologia", "inovação", "startups", "praia", "festa"]},
    {"continent": "Médio Oriente", "country": "Israel", "city": "Jerusalém", "lat": 31.7683, "lon": 35.2137, "tags": ["espiritualidade", "religião", "história", "fé", "conflito"]},
    {"continent": "Médio Oriente", "country": "Jordânia", "city": "Petra", "lat": 30.3285, "lon": 35.4444, "tags": ["mistério", "antiguidade", "deserto", "aventura"]},
    {"continent": "Médio Oriente", "country": "Jordânia", "city": "Amã", "lat": 31.9454, "lon": 35.9284, "tags": ["hospitalidade", "história", "cultura"]},
    {"continent": "Médio Oriente", "country": "Omã", "city": "Mascate", "lat": 23.5880, "lon": 58.3829, "tags": ["tranquilidade", "tradição", "mar", "paz"]},
    {"continent": "Médio Oriente", "country": "Barém", "city": "Manama", "lat": 26.2285, "lon": 50.5860, "tags": ["finanças", "pérolas", "ilhas"]},
    {"continent": "Médio Oriente", "country": "Kuwait", "city": "Cidade do Kuwait", "lat": 29.3759, "lon": 47.9774, "tags": ["riqueza", "petróleo", "comércio"]},

    # 6. ÁSIA
    {"continent": "Ásia", "country": "Índia", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "tags": ["fama", "cinema", "negócios", "multidão", "intensidade"]},
    {"continent": "Ásia", "country": "Índia", "city": "Nova Deli", "lat": 28.6139, "lon": 77.2090, "tags": ["poder", "política", "história", "caos", "transformação"]},
    {"continent": "Ásia", "country": "Índia", "city": "Goa", "lat": 15.2993, "lon": 74.1240, "tags": ["praia", "espiritualidade", "liberdade", "festa"]},
    {"continent": "Ásia", "country": "Índia", "city": "Jaipur", "lat": 26.9124, "lon": 75.7873, "tags": ["história", "realeza", "arquitetura", "joias"]},
    {"continent": "Ásia", "country": "Índia", "city": "Agra", "lat": 27.1767, "lon": 78.0081, "tags": ["romance", "amor", "monumentos"]},
    {"continent": "Ásia", "country": "Tailândia", "city": "Banguecoque", "lat": 13.7563, "lon": 100.5018, "tags": ["comércio", "diversão", "templos", "gastronomia"]},
    {"continent": "Ásia", "country": "Tailândia", "city": "Phuket", "lat": 7.8804, "lon": 98.3922, "tags": ["praia", "turismo", "lazer", "festa"]},
    {"continent": "Ásia", "country": "Tailândia", "city": "Chiang Mai", "lat": 18.7883, "lon": 98.9853, "tags": ["retiro", "cura", "espiritualidade", "templos", "natureza"]},
    {"continent": "Ásia", "country": "Vietname", "city": "Hanói", "lat": 21.0285, "lon": 105.8542, "tags": ["tradição", "história", "cultura", "gastronomia"]},
    {"continent": "Ásia", "country": "Vietname", "city": "Ho Chi Minh", "lat": 10.8231, "lon": 106.6297, "tags": ["negócios", "energia", "crescimento", "dinheiro"]},
    {"continent": "Ásia", "country": "Vietname", "city": "Da Nang", "lat": 16.0544, "lon": 108.2022, "tags": ["praia", "tecnologia", "pontes"]},
    {"continent": "Ásia", "country": "Camboja", "city": "Siem Reap", "lat": 13.3633, "lon": 103.8564, "tags": ["templos", "ruínas", "espiritualidade", "passado"]},
    {"continent": "Ásia", "country": "Camboja", "city": "Phnom Penh", "lat": 11.5564, "lon": 104.9282, "tags": ["renascimento", "história", "comércio"]},
    {"continent": "Ásia", "country": "Malásia", "city": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869, "tags": ["modernidade", "negócios", "compras", "mistura"]},
    {"continent": "Ásia", "country": "Malásia", "city": "Penang", "lat": 5.4164, "lon": 100.3327, "tags": ["gastronomia", "cultura", "patrimônio"]},
    {"continent": "Ásia", "country": "Singapura", "city": "Singapura", "lat": 1.3521, "lon": 103.8198, "tags": ["tecnologia", "dinheiro", "ordem", "limpeza", "finanças", "futuro"]},
    {"continent": "Ásia", "country": "Indonésia", "city": "Bali", "lat": -8.4095, "lon": 115.1889, "tags": ["espiritualidade", "cura", "natureza", "romance", "retiro", "bem-estar"]},
    {"continent": "Ásia", "country": "Indonésia", "city": "Jacarta", "lat": -6.2088, "lon": 106.8456, "tags": ["metrópole", "caos", "negócios", "crescimento"]},
    {"continent": "Ásia", "country": "Filipinas", "city": "Manila", "lat": 14.5995, "lon": 120.9842, "tags": ["comércio", "história", "hospitalidade"]},
    {"continent": "Ásia", "country": "Filipinas", "city": "Cebu", "lat": 10.3157, "lon": 123.8854, "tags": ["praia", "mergulho", "natureza"]},
    {"continent": "Ásia", "country": "China", "city": "Pequim", "lat": 39.9042, "lon": 116.4074, "tags": ["poder", "história", "política", "autoridade", "tradição"]},
    {"continent": "Ásia", "country": "China", "city": "Xangai", "lat": 31.2304, "lon": 121.4737, "tags": ["negócios", "finanças", "dinheiro", "futuro", "metrópole"]},
    {"continent": "Ásia", "country": "China", "city": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "tags": ["dinheiro", "comércio", "finanças", "tecnologia", "densidade"]},
    {"continent": "Ásia", "country": "China (Macau)", "city": "Macau", "lat": 22.1987, "lon": 113.5439, "tags": ["sorte", "cassinos", "dinheiro", "entretenimento", "jogos"]},
    {"continent": "Ásia", "country": "Japão", "city": "Tóquio", "lat": 35.6762, "lon": 139.6503, "tags": ["tecnologia", "ordem", "trabalho", "futuro", "metrópole", "eficiência"]},
    {"continent": "Ásia", "country": "Japão", "city": "Quioto", "lat": 35.0116, "lon": 135.7681, "tags": ["tradição", "espiritualidade", "templos", "paz", "cultura", "beleza"]},
    {"continent": "Ásia", "country": "Japão", "city": "Osaka", "lat": 34.6937, "lon": 135.5023, "tags": ["gastronomia", "comércio", "diversão", "pessoas"]},
    {"continent": "Ásia", "country": "Japão", "city": "Hokkaido", "lat": 43.2203, "lon": 142.8635, "tags": ["natureza", "frio", "neve", "esportes", "isolamento"]},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Seul", "lat": 37.5665, "lon": 126.9780, "tags": ["tecnologia", "beleza", "moda", "inovação", "dinheiro", "cultura pop"]},
    {"continent": "Ásia", "country": "Coreia do Sul", "city": "Busan", "lat": 35.1796, "lon": 129.0756, "tags": ["praia", "cinema", "mar", "comércio"]},
    {"continent": "Ásia", "country": "Taiwan", "city": "Taipé", "lat": 25.0330, "lon": 121.5654, "tags": ["tecnologia", "gastronomia", "organização", "inovação"]},

    # 7. OCEANIA & PACÍFICO
    {"continent": "Oceania", "country": "Austrália", "city": "Sydney", "lat": -33.8688, "lon": 151.2093, "tags": ["praia", "ação", "negócios", "beleza", "esporte", "lazer"]},
    {"continent": "Oceania", "country": "Austrália", "city": "Melbourne", "lat": -37.8136, "lon": 144.9631, "tags": ["arte", "cultura", "cafés", "criatividade"]},
    {"continent": "Oceania", "country": "Austrália", "city": "Brisbane", "lat": -27.4698, "lon": 153.0251, "tags": ["clima", "natureza", "bem-estar"]},
    {"continent": "Oceania", "country": "Austrália", "city": "Perth", "lat": -31.9505, "lon": 115.8605, "tags": ["isolamento", "praia", "mineração", "dinheiro"]},
    {"continent": "Oceania", "country": "Austrália", "city": "Uluru", "lat": -25.3444, "lon": 131.0369, "tags": ["espiritualidade", "misticismo", "terra", "isolamento", "sagrado"]},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Auckland", "lat": -36.8485, "lon": 174.7633, "tags": ["mar", "vela", "natureza", "comércio"]},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Queenstown", "lat": -45.0312, "lon": 168.6626, "tags": ["ação", "esporte", "aventura", "adrenalina", "natureza"]},
    {"continent": "Oceania", "country": "Nova Zelândia", "city": "Wellington", "lat": -41.2865, "lon": 174.7762, "tags": ["política", "vento", "cultura", "arte"]},
    {"continent": "Oceania", "country": "Fiji", "city": "Nadi", "lat": -17.8065, "lon": 177.4136, "tags": ["praia", "paraíso", "hospitalidade", "isolamento", "romance"]},
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Bora Bora", "lat": -16.5004, "lon": -151.7415, "tags": ["luxo", "romance", "lua de mel", "exclusividade", "praia"]},
    {"continent": "Oceania", "country": "Polinésia Francesa", "city": "Taiti", "lat": -17.6509, "lon": -149.4260, "tags": ["natureza", "mar", "beleza", "afastamento"]},
    {"continent": "Oceania", "country": "Havaí", "city": "Honolulu", "lat": 21.3069, "lon": -157.8583, "tags": ["praia", "surf", "natureza", "espírito aloha", "férias", "lazer"]},
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
            raise ValueError("Formato de data/hora inválido. Certifique-se de preencher os dados corretamente.")

# ========== GEOCODING BLINDADO (FALLBACK) ==========
# NOTA: Com a nova atualização do HTML, o frontend já envia lat e lon direto.
# Esta função agora existe apenas como um fallback absoluto caso algo falhe na comunicação.
def get_natal_coordinates(city_name):
    if not city_name or city_name.strip() == "":
        raise ValueError("O nome da cidade não pode estar vazio.")

    url_photon = f"https://photon.komoot.io/api/?q={city_name}&limit=1"
    try:
        resp = requests.get(url_photon, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data and "features" in data and len(data["features"]) > 0:
                coords = data["features"][0]["geometry"]["coordinates"]
                return coords[1], coords[0]
    except Exception as e:
        logger.warning(f"Aviso - Falha no Photon para {city_name}: {e}")

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
        logger.warning(f"Aviso - Falha no Nominatim para {city_name}: {e}")

    raise ValueError(f"CRÍTICO: O satélite não conseguiu precisar as coordenadas de '{city_name}'. O cálculo foi abortado por segurança (para não gerar um destino falso). Por favor, digite a cidade de forma mais específica no formato: 'Cidade, Estado, País'.")

# ========== FUSO HORÁRIO E DATA ==========

def get_timezone(lat, lon):
    tz_name = tz_finder.certain_timezone_at(lat=lat, lng=lon)
    if not tz_name:
        logger.warning(f"Fuso não encontrado para lat {lat}, lon {lon}. Usando UTC como segurança.")
        return pytz.UTC
    return pytz.timezone(tz_name)

def local_to_utc(lat, lon, local_datetime):
    tz = get_timezone(lat, lon)
    try:
        local_dt = tz.localize(local_datetime, is_dst=None)
    except pytz.exceptions.AmbiguousTimeError:
        # A hora repete-se na saída do horário de verão. Assume inverno.
        local_dt = tz.localize(local_datetime, is_dst=False)
    except pytz.exceptions.NonExistentTimeError:
        # BUG DO HORÁRIO FANTASMA CORRIGIDO: 
        # A hora foi "saltada" pela entrada do horário de verão e "não existe".
        # Solução: Adicionamos 1 hora e forçamos a leitura como DST.
        local_dt = tz.localize(local_datetime + timedelta(hours=1), is_dst=True)
    return local_dt.astimezone(pytz.UTC)

# ========== MOTORES MATEMÁTICOS DE ASTROLOGIA ==========

def calculate_solar_return(jd_natal, target_year, birth_month, birth_day):
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    
    try:
        start_date = datetime(target_year, birth_month, birth_day)
    except ValueError:
        # Blindagem Crítica: 29 de fev em ano não bissexto
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

def score_city_for_house(city_tags, house_id, user_intent):
    archetype_tags = HOUSE_ARCHETYPES.get(house_id, [])
    tag_score = 2 * len(set(city_tags) & set(archetype_tags))
    
    intent_score = 0
    if user_intent:
        intent_words = set(user_intent.lower().split())
        for word in intent_words:
            if len(word) > 3 and any(word in tag.lower() for tag in city_tags):
                intent_score += 1
                
    return tag_score + intent_score

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
        
        city_tags = city.get("tags", [])
        score = score_city_for_house(city_tags, house, user_intent)
        
        city_data = {
            "city": city["city"],
            "country": city["country"],
            "continent": city["continent"],
            "display_name": f"{city['city']}, {city['country']}",
            "lat": city["lat"],
            "lon": city["lon"],
            "tier": get_city_tier(city),
            "score": score
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
    # TRAVA DO VIAJANTE DO TEMPO CORRIGIDA
    if not (1900 <= int(target_year) <= 2100):
        raise ValueError("Ano astrológico fora do limite seguro (1900-2100). A operação foi abortada para proteger os motores astronómicos.")

    try:
        birth_local = parse_birth_datetime(natal_data['dob'], natal_data['time'])
        
        natal_lat = natal_data.get('natal_lat')
        natal_lon = natal_data.get('natal_lon')
        
        if natal_lat is None or natal_lon is None:
            natal_lat, natal_lon = get_natal_coordinates(natal_data['place_of_birth'])

        natal_lat = float(natal_lat)
        natal_lon = float(natal_lon)

        birth_utc = local_to_utc(natal_lat, natal_lon, birth_local)

        jd_natal = swe.julday(birth_utc.year, birth_utc.month, birth_utc.day,
                              birth_utc.hour + birth_utc.minute / 60.0)
        
        jd_return = calculate_solar_return(jd_natal, int(target_year), birth_local.month, birth_local.day)
        
        natal_cusps, _ = swe.houses_ex(jd_natal, natal_lat, natal_lon, b'P')
        
        return scan_premium_houses(jd_return, natal_cusps, user_intent)
    except Exception as e:
        logger.error(f"Erro no calculo matemático: {e}")
        raise e

# =====================================================================
# MOTOR DE INTELIGÊNCIA ARTIFICIAL (GEMINI)
# =====================================================================

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
        logger.error(f"ERRO CRÍTICO NO GEMINI: {e}")
        return ""
