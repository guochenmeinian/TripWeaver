from typing import Optional, List, Literal, Dict
from pydantic import BaseModel, Field, HttpUrl
from datetime import date, time, datetime
from google.genai import types
from geopy.point import Point

# === Retained setting ===
# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

# === Common Structures ===
class LocalizedString(BaseModel):
    """Localized string with optional translations for multilingual support."""
    default: str
    translations: Dict[str, str] = Field(default_factory=dict)


class SpotRelation(BaseModel):
    """Relation between this spot and another identified by ID."""
    related_id: str
    relation: str  # e.g., "10 minutes walk", "adjacent"


class TimeSlot(BaseModel):
    """Time slot suggestion for visiting a spot."""
    start: time
    end: time
    description: Optional[str] = None


class CostEstimate(BaseModel):
    """Estimated cost structure for an activity or location."""
    amount: float
    currency: str = "USD"
    per_person: bool = False
    description: Optional[str] = None


class Rating(BaseModel):
    """Rating and popularity data for a location or activity."""
    overall: float = Field(..., ge=0, le=5)
    popularity: Optional[float] = None
    user_rating: Optional[float] = None
    review_count: Optional[int] = None


class Location(BaseModel):
    """Geographic and descriptive location information."""
    name: str
    coordinates: Optional[Point] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


# === Core Structures ===
class Spot(BaseModel):
    """A point of interest or scheduled location on a trip."""
    id: str
    name: LocalizedString
    category: List[Literal["sightseeing", "food", "museum", "nature", "accommodation", "activity", "transport"]]
    location: Location
    description: Optional[LocalizedString] = None
    time_slot: TimeSlot
    duration_minutes: Optional[int] = None
    transit_time: Optional[int] = None
    cost: Optional[CostEstimate] = None
    rating: Optional[Rating] = None
    suggestions: List[LocalizedString] = Field(default_factory=list)
    related_spots: List[SpotRelation] = Field(default_factory=list)
    external_links: Dict[str, HttpUrl] = Field(default_factory=dict)
    notes: Optional[LocalizedString] = None
    confirmed: bool = False


class AttractionEvent(BaseModel):
    """A one-time event or fixed activity, such as a concert or workshop."""
    event_type: str = Field(default="visit")
    description: str
    address: str
    start_time: str
    end_time: str
    booking_required: bool = False
    price: Optional[str] = None


class DailyItinerary(BaseModel):
    """Daily agenda including weather, events, and suggested spots."""
    date: date
    city: str
    weather: Optional[Dict] = None
    theme: List[str] = Field(default_factory=list)
    spots: List[Spot] = Field(default_factory=list)
    events: List[AttractionEvent] = Field(default_factory=list)
    notes: Optional[LocalizedString] = None
    total_cost: Optional[CostEstimate] = None


class TravelerProfile(BaseModel):
    """Details about an individual traveler including preferences."""
    name: str
    age: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    preferences: Dict[str, str] = Field(default_factory=dict)
    allergies: List[str] = Field(default_factory=list)
    diet: List[str] = Field(default_factory=list)


class TripPlan(BaseModel):
    """Top-level structure representing a complete trip plan."""
    id: str
    title: LocalizedString
    start_date: date
    end_date: date
    traveler_count: int = 1
    traveler_profiles: List[TravelerProfile] = Field(default_factory=list)
    transport_mode: Literal["car", "train", "flight", "mixed"] = "car"
    budget_level: Literal["budget", "midrange", "luxury"] = "midrange"
    cities: List[str]
    itinerary: List[DailyItinerary]
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    version: str = "1.0.0"
    metadata: Dict = Field(default_factory=dict)


class PackingList(BaseModel):
    """Recommended items to bring based on trip context."""
    items: List[str]


# === POI Suggestions (used in LLM tool output) ===
class POI(BaseModel):
    """External recommendation data for places of interest."""
    place_name: str
    address: str
    lat: float
    lng: float
    review_ratings: str
    highlights: str
    image_url: str
    map_url: Optional[str] = None
    place_id: Optional[str] = None


class POISuggestions(BaseModel):
    """List of recommended points of interest."""
    places: List[POI]
