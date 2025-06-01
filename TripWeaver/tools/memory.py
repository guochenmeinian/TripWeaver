# tools/memory.py

from datetime import datetime
import json
import os
from typing import Dict, Any, Optional, Callable

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from TripWeaver.shared_libraries import constants
from TripWeaver.shared_libraries.types import TripPlan
from pydantic import ValidationError

# Path to initial scenario file
SAMPLE_SCENARIO_PATH = os.getenv(
    "TRAVEL_CONCIERGE_SCENARIO", "TripWeaver/profiles/itinerary_empty_default.json"
)

# Key used in memory state for storing the trip plan
TRIP_PLAN_KEY = "trip_plan"


def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Append a value to a list in session memory under the given key, avoiding duplicates.
    """
    state = tool_context.state
    if key not in state:
        state[key] = []
    if value not in state[key]:
        state[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Store a key-value pair in session memory, replacing any existing value.
    """
    tool_context.state[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Remove a value from a list in session memory under the given key.
    """
    state = tool_context.state
    if state.get(key) is None:
        state[key] = []
    if value in state[key]:
        state[key].remove(value)
    return {"status": f'Removed "{key}": "{value}"'}


def get_trip_plan(state: State) -> Optional[TripPlan]:
    """
    Retrieve the TripPlan object from session state.
    """
    raw = state.get(TRIP_PLAN_KEY)
    if raw:
        try:
            return TripPlan.parse_obj(raw)
        except ValidationError as e:
            print(f"TripPlan validation error: {e}")
            return None
    return None


def set_trip_plan(state: State, plan: TripPlan) -> None:
    """
    Store a TripPlan object into session state.
    """
    state[TRIP_PLAN_KEY] = json.loads(plan.json())


def update_trip_plan(state: State, update_fn: Callable[[TripPlan], None]) -> Optional[TripPlan]:
    """
    Update the TripPlan in session memory using a provided update function.
    """
    plan = get_trip_plan(state)
    if not plan:
        return None
    update_fn(plan)
    set_trip_plan(state, plan)
    return plan


def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Initialize session state using a dictionary of pre-defined keys and values.
    """
    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.ITIN_INITIALIZED not in target:
        target[constants.ITIN_INITIALIZED] = True
        target.update(source)

        itinerary = source.get(constants.ITIN_KEY, {})
        if itinerary:
            target[constants.ITIN_START_DATE] = itinerary.get(constants.START_DATE)
            target[constants.ITIN_END_DATE] = itinerary.get(constants.END_DATE)
            target[constants.ITIN_DATETIME] = itinerary.get(constants.START_DATE)


def _load_precreated_itinerary(callback_context: CallbackContext):
    """
    Load the initial scenario JSON and populate session state.
    Used as the `before_agent_callback` hook in root agent.
    """
    with open(SAMPLE_SCENARIO_PATH, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")
    _set_initial_states(data["state"], callback_context.state)
