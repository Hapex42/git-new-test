"""Search Marine Corps League detachments near Jacksonville, Florida.

Replace detachments.csv with the official detachment list.
"""

from __future__ import annotations

import csv
import math
import pathlib
import re
import sys
from dataclasses import dataclass

JACKSONVILLE_LAT = 30.3322
JACKSONVILLE_LON = -81.6557
RADIUS_MILES = 100.0

REQUIRED_FIELDS = {
    "detachment_number",
    "name",
    "city",
    "state",
    "latitude",
    "longitude",
}


@dataclass(frozen=True)
class Detachment:
    number: str
    name: str
    city: str
    state: str
    latitude: float
    longitude: float


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_miles = 3958.7613
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_miles * c


def detachment_sort_key(value: str) -> list[tuple[int, object]]:
    parts = re.split(r"(\d+)", value)
    key: list[tuple[int, object]] = []
    for part in parts:
        if not part:
            continue
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part.lower()))
    return key


def load_detachments(csv_path: pathlib.Path) -> list[Detachment]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV file is missing a header row.")

        missing = REQUIRED_FIELDS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "CSV file is missing required columns: "
                + ", ".join(sorted(missing))
            )

        detachments: list[Detachment] = []
        for line_number, row in enumerate(reader, start=2):
            if not row:
                continue
            if not any(value.strip() for value in row.values() if value):
                continue

            try:
                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
            except ValueError as exc:
                raise ValueError(
                    f"Invalid latitude/longitude on line {line_number}."
                ) from exc

            detachments.append(
                Detachment(
                    number=row["detachment_number"].strip(),
                    name=row["name"].strip(),
                    city=row["city"].strip(),
                    state=row["state"].strip(),
                    latitude=latitude,
                    longitude=longitude,
                )
            )

    return detachments


def search_detachments(
    detachments: list[Detachment],
    center_lat: float,
    center_lon: float,
    radius_miles: float,
) -> list[Detachment]:
    nearby: list[Detachment] = []
    for detachment in detachments:
        distance = haversine_miles(
            center_lat,
            center_lon,
            detachment.latitude,
            detachment.longitude,
        )
        if distance <= radius_miles:
            nearby.append(detachment)
    return nearby


def format_detachments(detachments: list[Detachment]) -> str:
    lines: list[str] = []
    for detachment in detachments:
        location = detachment.city
        if detachment.state:
            location = f"{location}, {detachment.state}"
        lines.append(f"{detachment.number} {detachment.name} - {location}")
    return "\n".join(lines)


def main() -> int:
    csv_path = pathlib.Path(__file__).with_name("detachments.csv")
    if len(sys.argv) > 1:
        csv_path = pathlib.Path(sys.argv[1])

    detachments = load_detachments(csv_path)
    nearby = search_detachments(
        detachments,
        JACKSONVILLE_LAT,
        JACKSONVILLE_LON,
        RADIUS_MILES,
    )
    nearby_sorted = sorted(nearby, key=lambda item: detachment_sort_key(item.number))
    output = format_detachments(nearby_sorted)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
