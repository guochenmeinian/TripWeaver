from typing import Optional, List, Literal, Dict, Union, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import date, time, datetime
from google.genai import types

# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


class Location(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class TimeSlot(BaseModel):
    start_time: str  # "09:00"
    end_time: str    # "10:30"
    description: Optional[str] = None


class Spot(BaseModel):
    id: str
    name: str
    category: str  # one of sightseeing, food, museum, nature, activity
    location_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    rating: Optional[float] = None
    image_url: Optional[str] = None


class SpotSuggestions(BaseModel):
    spots: List[Spot]


class HomeAddress(BaseModel):
    event_type: str
    address: str
    local_prefer_mode: str


class UserProfile(BaseModel):
    passport_nationality: str
    seat_preference: str
    food_preference: str
    allergies: List[str]
    likes: List[str]
    dislikes: List[str]
    price_sensitivity: List[str]
    home: HomeAddress


class HousingOption(BaseModel):
    name: str
    price_per_night: str
    location: str
    url: Optional[str] = None
    description: Optional[str] = None
    num_beds: str

class HousingResults(BaseModel):
    housing_options: List[HousingOption]


class BasicTripEntry(BaseModel):
    city: str = Field(..., description="Name of the city")
    check_in: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    transit_from_previous: str = Field(..., description="How the user will arrive from the previous city")

class BasicTripPlanSchema(BaseModel):
    trip_plan: List[BasicTripEntry]

    

class CostEstimate(BaseModel):
    amount: float
    currency: str = "USD"
    per_person: bool = False
    description: Optional[str] = None


class Rating(BaseModel):
    overall: float = Field(..., ge=0, le=5)
    popularity: Optional[float] = None
    user_rating: Optional[float] = None
    review_count: Optional[int] = None


class Location(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class POI(BaseModel):
    """A Point Of Interest suggested by the agent."""
    place_name: str = Field(description="Name of the attraction")
    address: str = Field(
        description="An address or sufficient information to geocode for a Lat/Lon"
    )
    lat: str = Field(
        description="Numerical representation of Latitude of the location (e.g., 20.6843)"
    )
    long: str = Field(
        description="Numerical representation of Longitude of the location (e.g., -88.5678)"
    )
    review_ratings: str = Field(
        description="Numerical representation of rating (e.g. 4.8 , 3.0 , 1.0 etc)"
    )
    highlights: str = Field(description="Short description highlighting key features")
    image_url: str = Field(description="verified URL to an image of the destination")
    map_url: Optional[str] = Field(description="Verified URL to Google Map")
    place_id: Optional[str] = Field(description="Google Map place_id")


class POISuggestions(BaseModel):
    """Points of interest recommendation."""
    places: list[POI]
    



