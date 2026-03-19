import swisseph as swe
import requests
import time
from functools import lru_cache
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
swe.set_ephe_path('/usr/share/sweph/ephe')

def calculate_solar_return(jd_natal, target_year):
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    jd_start = swe.julday(target_year, 1, 1, 12.0)
    return swe.solcross_ut(sun_longitude, jd_start)

def calculate_house_position(jd_ut, longitude, latitude):
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    cusps_list = list(cusps) + [cusps[0] + 360]
    sun_pos, _ = swe.calc_ut(jd_ut, swe.SUN)
    sun_adj = sun_pos[0]
    if sun_adj < cusps_list[0]:
        sun_adj += 360
    for i in range(12):
        if cusps_list[i] <= sun_adj < cusps_list[i+1]:
            return i+1
    return 1

def cluster_longitudes(longitudes, tolerance=5.0):
    if not longitudes:
        return []
    longitudes.sort()
    clusters = []
    current_cluster = [longitudes[0]]
    for lon in longitudes[1:]:
        if lon - current_cluster[-1] <= tolerance:
            current_cluster.append(lon)
        else:
            avg_lon = sum(current_cluster) / len(current_cluster)
            clusters.append(avg_lon)
            current_cluster = [lon]
    if current_cluster:
        avg_lon = sum(current_cluster) / len(current_cluster)
        clusters.append(avg_lon)
    return clusters

@lru_cache(maxsize=128)
def cached_reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "accept-language": "pt-BR"
    }
    headers = {"User-Agent": "ProtocoloSolar/1.0 (contato@seudominio.com)"}
    time.sleep(1.1)
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            city = (address.get('city') or address.get('town') or
                    address.get('village') or address.get('hamlet') or
                    address.get('municipality') or '')
            state = address.get('state', '')
            country = address.get('country', '')
            return {
                "display_name": data.get('display_name', ''),
                "city": city,
                "state": state,
                "country": country,
                "lat": lat,
                "lon": lon
            }
    except Exception as e:
        print(f"Erro no geocoding: {e}")
    return None

def scan_all_houses(jd_return, latitude_natal, step=2.0):
    house_longitudes = {i: [] for i in range(1, 13)}
    lon = -180.0
    while lon <= 180.0:
        house = calculate_house_position(jd_return, lon, latitude_natal)
        if 1 <= house <= 12:
            house_longitudes[house].append(lon)
        lon += step

    results = {}
    for house, lons in house_longitudes.items():
        if not lons:
            results[house] = None
            continue
        clusters = cluster_longitudes(lons, tolerance=5.0)
        if clusters:
            best_lon = clusters[0]
            city_info = cached_reverse_geocode(latitude_natal, best_lon)
            results[house] = {
                "city": city_info,
                "longitude": best_lon
            }
        else:
            results[house] = None
    return results

def find_best_city_for_house(natal_data, target_year, target_house):
    # Esta função mantém compatibilidade com a rota antiga
    birth_date = datetime.strptime(natal_data['dob'] + ' ' + natal_data['time'], '%d/%m/%Y %H:%M')
    jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                          birth_date.hour + birth_date.minute/60.0)
    latitude_natal = natal_data.get('latitude', -23.55)
    jd_return = calculate_solar_return(jd_natal, target_year)
    # Usa a varredura para todas as casas e filtra pela target_house
    todas = scan_all_houses(jd_return, latitude_natal, step=2.0)
    return todas.get(target_house, {"city": None, "longitude": None})
