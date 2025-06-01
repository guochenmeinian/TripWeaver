# tools/convert.py

from TripWeaver.shared_libraries.types import GeminiSpot, Spot
from datetime import time
from TripWeaver.shared_libraries.types import LocalizedString, Location, TimeSlot, Rating

# Add conversion helper from FlatSpot → Spot
# (for use by the itinerary planner or internal logic)

def gemini_spot_to_spot(gemini_spot: GeminiSpot) -> Spot:
    return Spot(
        id="spot-" + gemini_spot.name.lower().replace(" ", "-"),
        name=LocalizedString(default=gemini_spot.name),
        category=[gemini_spot.category],
        location=Location(name=gemini_spot.name),
        description=LocalizedString(default=gemini_spot.description or "") if gemini_spot.description else None,
        time_slot=TimeSlot(start=time(9, 0), end=time(11, 0)),
        rating=Rating(overall=gemini_spot.rating or 4.0) if gemini_spot.rating else None,
        confirmed=False
    )