import swisseph as swe
import math
from datetime import datetime
import requests
import time

def calculate_solar_return(jd_natal, target_year):
    sun_pos, _ = swe.calc_ut(jd_natal, swe.SUN)
    sun_longitude = sun_pos[0]
    jd_start = swe.julday(target_year, 1, 1, 12.0)
    jd_return = swe.solcross_ut(sun_longitude, jd_start)
    return jd_return

def calculate_house_position(jd_ut, longitude, latitude):
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P')
    # Adiciona 360° à última cúspide para facilitar a comparação
    cusps_list = list(cusps) + [cusps[0] + 360]
    sun_pos, _ = swe.calc_ut(jd_ut, swe.SUN)
    sun_longitude = sun_pos[0]
    # Ajusta a longitude do Sol se necessário
    sun_adj = sun_longitude
    # Encontra em qual casa o Sol está
    for i in range(12):
        if cusps_list[i] <= sun_adj < cusps_list[i+1]:
            return i+1
    # Se não encontrar (pode ocorrer próximo a 0°), ajusta
    if sun_adj < cusps_list[0]:
        sun_adj += 360
        for i in range(12):
            if cusps_list[i] <= sun_adj < cusps_list[i+1]:
                return i+1
    return 1  # fallback

def scan_longitudes_for_house(jd_return, latitude_natal, target_house, step=2.0):
    results = []
    lon = -180.0
    while lon <= 180.0:
        house = calculate_house_position(jd_return, lon, latitude_natal)
        if house == target_house:
            results.append(lon)
        lon += step
    return results

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

def reverse_geocode_nominatim(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "accept-language": "pt-BR"
    }
    headers = {
        "User-Agent": "ProtocoloSolar/1.0 (seu-email@exemplo.com)"
    }
    time.sleep(1)
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            city = (address.get('city') or address.get('town') or 
                   address.get('village') or address.get('hamlet') or '')
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

def find_best_city_for_house(natal_data, target_year, target_house):
    swe.set_ephe_path('/usr/share/sweph/ephe')
    birth_date = datetime.strptime(natal_data['dob'] + ' ' + natal_data['time'], '%d/%m/%Y %H:%M')
    jd_natal = swe.julday(birth_date.year, birth_date.month, birth_date.day,
                          birth_date.hour + birth_date.minute/60.0)
    latitude_natal = natal_data.get('latitude', -23.55)
    jd_return = calculate_solar_return(jd_natal, target_year)
    candidate_lons = scan_longitudes_for_house(jd_return, latitude_natal, target_house)
    clusters = cluster_longitudes(candidate_lons)
    cities = []
    for cluster_lon in clusters:
        city_info = reverse_geocode_nominatim(latitude_natal, cluster_lon)
        if city_info:
            cities.append(city_info)
    return {
        "target_house": target_house,
        "target_year": target_year,
        "cities": cities,
        "raw_clusters": clusters,
        "candidate_longitudes": candidate_lons[:10]
    }
