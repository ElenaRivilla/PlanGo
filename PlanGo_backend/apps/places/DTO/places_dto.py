from dataclasses import dataclass, asdict
from typing import Optional, List, Iterable


@dataclass
class AccommodationDetailDTO:
    accommodation: str
    id: str
    accommodaton_type: Optional[str]
    address: Optional[str]
    rating: float
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[str]
    isSave: Optional[bool]


@dataclass
class RestaurantDetailDTO:
    restaurant: str
    id: str
    restaurant_type: Optional[str]
    address: Optional[str]
    rating: float
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[str]
    isSave: Optional[bool]


@dataclass
class ActivityDetailDTO:
    activity: str
    place_id: str
    activity_type: Optional[str]
    address: Optional[str]
    rating: float
    latitude: Optional[float]
    longitude: Optional[float]
    images: List[str]
    isSave: Optional[bool]


def map_accommodation_detail(acc, images: List[str]) -> dict:
    return asdict(AccommodationDetailDTO(
        accommodation=acc.name,
        id=acc.place_id,
        accommodaton_type=acc.accomodation_type,
        address=acc.address,
        rating=acc.rating if acc.rating is not None else 3.0,
        latitude=acc.latitude,
        longitude=acc.longitude,
        images=images,
        isSave=acc.isSave,
    ))


def map_restaurant_detail(rest, images: List[str]) -> dict:
    return asdict(RestaurantDetailDTO(
        restaurant=rest.name,
        id=rest.place_id,
        restaurant_type=rest.restaurant_type,
        address=rest.address,
        rating=rest.rating if rest.rating is not None else 3.0,
        latitude=rest.latitude,
        longitude=rest.longitude,
        images=images,
        isSave=rest.isSave,
    ))


def map_activity_detail(act, images: List[str]) -> dict:
    return asdict(ActivityDetailDTO(
        activity=act.name,
        place_id=act.place_id,
        activity_type=act.activity_type,
        address=act.address,
        rating=act.rating if act.rating is not None else 3.0,
        latitude=act.latitude,
        longitude=act.longitude,
        images=images,
        isSave=act.isSave,
    ))
