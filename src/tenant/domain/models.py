from dataclasses import dataclass
from typing import Optional


@dataclass
class TenantUser:
    id: Optional[int]
    email: str
    hashed_password: str
    is_active: bool = True
    display_name: Optional[str] = None
