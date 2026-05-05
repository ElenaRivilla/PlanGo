import requests
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env')
OVERPASS_URL = os.getenv("OVERPASS_API_URL")

OVERPASS_MIRRORS = [
    OVERPASS_URL,
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

def map_category_to_osm_tags(category: str) -> dict:
    cat = category.strip().lower()

    if cat in ('alojamientos', 'alojamiento', 'accommodations', 'lodging'):
        return {
            'amenity': ['hotel', 'hostel', 'motel', 'guest_house'],
            'tourism': ['hotel', 'hostel', 'chalet', 'apartment', 'guest_house', 'camp_site'],
        }

    if cat in ('comer y beber', 'comer', 'restaurantes', 'food', 'drink'):
        return {
            'amenity': ['restaurant', 'cafe', 'bar', 'pub', 'fast_food', 'food_court', 'biergarten'],
        }

    if cat in ('cosas que hacer', 'actividades', 'atracciones', 'things to do', 'activities'):
        return {
            'tourism': ['museum', 'attraction', 'gallery', 'zoo', 'aquarium', 'theme_park'],
            'amenity': ['theatre', 'cinema', 'arts_centre', 'nightclub'],
            'leisure': ['park', 'garden', 'nature_reserve', 'stadium'],
        }

    return {}


def build_overpass_query(lat: float, lng: float, radius: int, tag_groups: dict) -> str:
    parts = []
    for key, values in tag_groups.items():
        for value in values:
            parts.append(f'  node["{key}"="{value}"](around:{radius},{lat},{lng});')
    return '[out:json][timeout:30];\n(\n' + '\n'.join(parts) + '\n);\nout center 25;'


def parse_element(element: dict) -> dict | None:
    tags = element.get('tags', {})
    name = tags.get('name') or tags.get('name:es') or tags.get('name:en')
    if not name:
        return None

    if element['type'] == 'node':
        lat = element.get('lat')
        lon = element.get('lon')
    else:
        center = element.get('center', {})
        lat = center.get('lat')
        lon = center.get('lon')

    if lat is None or lon is None:
        return None

    addr_parts = []
    if tags.get('addr:street'):
        street = tags['addr:street']
        if tags.get('addr:housenumber'):
            street += ' ' + tags['addr:housenumber']
        addr_parts.append(street)
    if tags.get('addr:city'):
        addr_parts.append(tags['addr:city'])

    primary_type = tags.get('amenity') or tags.get('tourism') or tags.get('leisure') or ''

    return {
        'id': f"{element['type']}/{element['id']}",
        'displayName': {'text': name},
        'location': {'latitude': lat, 'longitude': lon},
        'formattedAddress': ', '.join(addr_parts),
        'rating': None,
        'photos': [],
        'primaryType': primary_type,
        'isSave': False,
    }


def search_nearby(lat: float, lng: float, radius: int, category: str) -> list:
    tag_groups = map_category_to_osm_tags(category)
    if not tag_groups:
        return []

    query = build_overpass_query(lat, lng, radius, tag_groups)
    headers = {
        'Accept': '*/*',
        'User-Agent': 'PlanGo/1.0'
    }

    last_error = None
    for url in OVERPASS_MIRRORS:
        if not url:
            continue
        try:
            response = requests.post(url, data=query, headers=headers, timeout=35)
            response.raise_for_status()
            elements = response.json().get('elements', [])
            places = [parse_element(e) for e in elements]
            return [p for p in places if p is not None]
        except requests.exceptions.Timeout:
            last_error = f"Timeout en {url}"
            continue
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code in (429, 504):
                last_error = f"Error {e.response.status_code} en {url}"
                continue
            raise

    raise requests.exceptions.ConnectionError(f"Todos los mirrors fallaron. Último error: {last_error}")


def attach_is_save_flag(places: list, saved_place_ids: set) -> list:
    for place in places:
        place['isSave'] = place['id'] in saved_place_ids
    return places
