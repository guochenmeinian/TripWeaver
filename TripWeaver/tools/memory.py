# tools/memory.py

from datetime import datetime
import json
import os
from typing import Dict, Any, Optional, Callable

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from TripWeaver.shared_libraries import constants
from pydantic import ValidationError

# Path to initial scenario file
SAMPLE_SCENARIO_PATH = os.getenv(
    "TRAVEL_CONCIERGE_SCENARIO", "TripWeaver/profiles/itinerary_empty_default.json"
)

# Key used in memory state for storing the trip plan
TRIP_PLAN_KEY = "trip_plan"

def get_by_path(state: dict, path: str, delimiter: str = "/") -> dict:
    keys = path.split(delimiter)
    current = state
    for k in keys:
        current = current.setdefault(k, {})
    return current


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


def mark_checklist_done(item: str, tool_context: ToolContext):
    if tool_context.state.get("current_agent") != "planning_agent":
        return {"error": f"Checklist update not allowed: current agent is {tool_context.state.get('current_agent')}"}
    checklist = tool_context.state.get("planning_checklist", {})
    if item not in checklist:
        return {"error": f"Invalid checklist item: {item}"}
    checklist[item] = True
    return {"status": f"Marked '{item}' as done."}


def is_checklist_complete(tool_context: ToolContext) -> bool:
    if tool_context.state.get("current_agent") != "planning_agent":
        return False
    checklist = tool_context.state.get("planning_checklist", {})
    return all(checklist.get(k, False) for k in [
        "weather_fetched",
        "places_selected",
        "places_info_fetched",
        "distances_calculated",
        "places_grouped",
        "proximity_search_done",
        "lodging_fetched"
    ])