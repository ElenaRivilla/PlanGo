from dataclasses import dataclass, asdict
from typing import Iterable, List, Dict, Optional
from datetime import date, datetime
from ..models.destination import Destination

@dataclass
class ItineraryDTO:
    itinerary_id: int
    itinerary_name: str
    creator_user: Optional[int]
    creation_date: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    countries: List[str]
    destinations_count: Optional[int] = None

def _iso(date: Optional[date | datetime]) -> Optional[str]:
    if date is None:
        return None
    try:
        return date.isoformat()
    except Exception:
        return str(date)

def map_itinerary(it) -> Dict:
    creator = getattr(it.creator_user, 'id', it.creator_user) if hasattr(it, 'creator_user') else None
    countries_str = getattr(it, 'countries', '') or ''
    countries = [c.strip() for c in countries_str.split(',') if c.strip()]
    destinations_count = Destination.objects.filter(itinerary=it).count()  # Contar destinos directamente

    dto = ItineraryDTO(
        itinerary_id=getattr(it, 'itinerary_id', getattr(it, 'id', None)),
        itinerary_name=getattr(it, 'itinerary_name', ''),
        creator_user=creator,
        creation_date=_iso(getattr(it, 'creation_date', None)),
        start_date=_iso(getattr(it, 'start_date', None)),
        end_date=_iso(getattr(it, 'end_date', None)),
        countries=countries,
        destinations_count=destinations_count
    )
    return asdict(dto)

def map_itineraries(destinations: Iterable) -> List[Dict]:
    return [map_itinerary(destination) for destination in destinations]