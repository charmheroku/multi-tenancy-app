from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str
    hashed_password: str
    is_active: bool = True
    is_owner: bool = False


@dataclass
class Organization:
    id: int
    name: str
    owner_id: int
    db_url: str
