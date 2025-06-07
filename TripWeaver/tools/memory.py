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

from datetime import datetime, timedelta

# Path to initial scenario file
EMPTY_SCENARIO_PATH = os.getenv(
    "TRAVEL_CONCIERGE_SCENARIO", "TripWeaver/profiles/empty_profile.json"
)
SAMPLE_SCENARIO_PATH = os.getenv(
    "TRAVEL_CONCIERGE_SCENARIO", "TripWeaver/profiles/sample_profile.json"
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




def _expand_trip_plan_to_daily_itinerary(callback_context: CallbackContext):
    """
    After-agent callback: use trip_plan to create daily_itinerary_plan.
    Runs after pre_trip_agent completes and user_profile is available.
    """
    state = callback_context.state
    profile = state.memory.get("user_profile", {})
    trip_plan = profile.get("trip_plan", [])
    daily_plan = []

    for leg in trip_plan:
        city = leg.get("city")
        check_in = leg.get("check_in")
        check_out = leg.get("check_out")
        if not city or not check_in or not check_out:
            continue

        s = datetime.strptime(check_in, "%Y-%m-%d")
        e = datetime.strptime(check_out, "%Y-%m-%d")

        while s < e:
            daily_plan.append({
                "date": s.strftime("%Y-%m-%d"),
                "city": city,
                "spots": [],
                "events": [],
                "notes": ""
            })
            s += timedelta(days=1)

    state.memory["daily_itinerary_plan"] = daily_plan
    print(f"\n✅ Daily itinerary initialized from trip_plan: {daily_plan}\n")
