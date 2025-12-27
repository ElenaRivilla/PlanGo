from dataclasses import dataclass, asdict
from typing import Optional, List, Iterable
from datetime import date, datetime

@dataclass
class DestinationDTO:
    destination_id: int
    itinerary_id: Optional[str]
    country: Optional[str]
    city_name: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

def _iso(date: Optional[date | datetime]) -> Optional[str]:
    if date is None:
        return None
    try:
        return date.isoformat()
    except Exception:
        return str(date)

def map_destination(dest) -> DestinationDTO:
    itinerary_val = getattr(dest.itinerary, 'itinerary_id', dest.itinerary)
    
    return DestinationDTO(
        destination_id=getattr(dest, 'id', None),
        itinerary_id=itinerary_val,
        country=getattr(dest, 'country', None),
        city_name=getattr(dest, 'city_name', None),
        start_date=_iso(getattr(dest, 'start_date', None)),
        end_date=_iso(getattr(dest, 'end_date', None)),
        latitude=getattr(dest, 'latitude', None),
        longitude=getattr(dest, 'longitude', None),
    )

def map_destinations(destinations: Iterable) -> List[dict]:
    return [asdict(map_destination(destination)) for destination in destinations]