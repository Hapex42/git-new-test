from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable, List


JACKSONVILLE_LAT = 30.3322
JACKSONVILLE_LON = -81.6557
SEARCH_RADIUS_MILES = 100.0


@dataclass(frozen=True)
class Detachment:
    number: str
    name: str
    city: str
    state: str
    lat: float
    lon: float


DETACHMENTS: List[Detachment] = [
    Detachment(
        number="003",
        name="First Coast Detachment",
        city="Jacksonville",
        state="FL",
        lat=30.3322,
        lon=-81.6557,
    ),
    Detachment(
        number="9",
        name="Amelia Island Detachment",
        city="Fernandina Beach",
        state="FL",
        lat=30.6697,
        lon=-81.4626,
    ),
    Detachment(
        number="12",
        name="Ancient City Detachment",
        city="St. Augustine",
        state="FL",
        lat=29.9012,
        lon=-81.3124,
    ),
    Detachment(
        number="12A",
        name="Camden County Detachment",
        city="Kingsland",
        state="GA",
        lat=30.7999,
        lon=-81.6898,
    ),
    Detachment(
        number="101",
        name="Golden Isles Detachment",
        city="Brunswick",
        state="GA",
        lat=31.1499,
        lon=-81.4915,
    ),
    Detachment(
        number="105",
        name="Palatka River Detachment",
        city="Palatka",
        state="FL",
        lat=29.6486,
        lon=-81.6376,
    ),
    Detachment(
        number="210",
        name="Gator Country Detachment",
        city="Lake City",
        state="FL",
        lat=30.1897,
        lon=-82.6393,
    ),
    Detachment(
        number="300",
        name="Central Florida Detachment",
        city="Orlando",
        state="FL",
        lat=28.5383,
        lon=-81.3792,
    ),
    Detachment(
        number="450",
        name="Capital City Detachment",
        city="Tallahassee",
        state="FL",
        lat=30.4383,
        lon=-84.2807,
    ),
    Detachment(
        number="511",
        name="Coastal Empire Detachment",
        city="Savannah",
        state="GA",
        lat=32.0809,
        lon=-81.0912,
    ),
]


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_miles = 3958.8
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_miles * c


def alphanum_key(value: str) -> List[object]:
    parts = re.split(r"(\d+)", value)
    key: List[object] = []
    for part in parts:
        if not part:
            continue
        key.append(int(part) if part.isdigit() else part.lower())
    return key


def detachments_within_radius(
    detachments: Iterable[Detachment],
    origin_lat: float,
    origin_lon: float,
    radius_miles: float,
) -> List[Detachment]:
    within_radius = []
    for detachment in detachments:
        distance = haversine_miles(
            origin_lat, origin_lon, detachment.lat, detachment.lon
        )
        if distance <= radius_miles:
            within_radius.append(detachment)
    return sorted(within_radius, key=lambda det: alphanum_key(det.number))


def search_jacksonville_area() -> List[str]:
    nearby = detachments_within_radius(
        DETACHMENTS, JACKSONVILLE_LAT, JACKSONVILLE_LON, SEARCH_RADIUS_MILES
    )
    return [
        f"{det.number} - {det.name} - {det.city}"
        for det in nearby
    ]


if __name__ == "__main__":
    for line in search_jacksonville_area():
        print(line)
