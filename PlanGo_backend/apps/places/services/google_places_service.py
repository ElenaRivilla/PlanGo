from typing import List, Dict, Any

def map_category_to_types(category: str) -> List[str]:
	if not category:
		return []
	cat = category.strip().lower()

	if cat in ("alojamientos", "alojamiento", "accommodations", "lodging"):
		return [
			"lodging", "hotel", "motel", "bed_and_breakfast", "guest_house", "hostel",
			"resort_hotel", "campground", "inn"
		]

	if cat in ("comer y beber", "comer", "restaurantes", "food", "drink"):
		return [
			"restaurant", "bar", "cafe", "bakery", "pub", "fast_food_restaurant",
			"buffet_restaurant", "food_court", "meal_takeaway", "meal_delivery"
		]

	if cat in ("cosas que hacer", "actividades", "atracciones", "things to do", "activities"):
		return [
			"tourist_attraction", "museum", "art_gallery", "zoo", "aquarium", "park",
			"amusement_park", "night_club", "church", "mosque"
		]

	return []

def build_search_payload(lat: float, lng: float, radius: int, included_types: List[str]) -> Dict[str, Any]:
	return {
		"includedTypes": included_types,
		"locationRestriction": {
			"circle": {
				"center": {"latitude": lat, "longitude": lng},
				"radius": radius
			}
		},
	}

def attach_is_save_flag_to_places(api_response: Dict[str, Any], saved_place_ids: set) -> Dict[str, Any]:
	if not api_response or 'places' not in api_response:
		return api_response

	for place in api_response.get('places', []):
		place['isSave'] = place.get('id') in saved_place_ids
	return api_response