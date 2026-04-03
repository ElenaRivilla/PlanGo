from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class UserDTO:
    id: int
    email: str
    first_name: str
    last_name: str
    user_image: Optional[str]


@dataclass
class ParticipantDTO:
    participant_id: Optional[int]
    destination_id: int
    user: Optional[int]
    participant_name: str
    is_user: bool


def map_user(user) -> dict:
    return asdict(UserDTO(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        user_image=user.user_image,
    ))


def map_participant(p, is_user: bool = False) -> dict:
    return asdict(ParticipantDTO(
        participant_id=getattr(p, 'participant_id', None),
        destination_id=p.destination.id if hasattr(p, 'destination') and p.destination else p,
        user=p.user.id if getattr(p, 'user', None) else None,
        participant_name=p.participant_name,
        is_user=is_user,
    ))
