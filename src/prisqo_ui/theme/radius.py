"""Border radius scale used throughout PRISQO UI Kit."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Radius:
    SM: int = 4
    MD: int = 8
    LG: int = 12
    XL: int = 16
    ROUND: int = 999


RADIUS = Radius()
