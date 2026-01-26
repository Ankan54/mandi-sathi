from crewai.tools import tool
from typing import List
from difflib import get_close_matches
from utils.api_client import DataGovAPIClient

# Common state and district mappings for India
INDIAN_STATES = {
    "uttar pradesh": ["Ballia", "Varanasi", "Lucknow", "Kanpur", "Agra", "Meerut", "Allahabad"],
    "maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur"],
    "punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
    "haryana": ["Faridabad", "Gurgaon", "Rohtak", "Panipat", "Karnal"],
    "madhya pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain"],
    "rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Udaipur"],
    "gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    "west bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"],
    "karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
    "tamil nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
}

# Normalize state names
STATE_ALIASES = {
    "up": "uttar pradesh",
    "mp": "madhya pradesh",
    "wb": "west bengal",
    "tn": "tamil nadu",
    "mh": "maharashtra",
}

@tool("Get Districts for State")
def get_districts_for_state(state_name: str) -> str:
    """
    Get list of valid district names for a given state.
    Handles spelling variations and returns corrected district names.
    Fetches from data.gov.in API with fallback to hardcoded list.

    Args:
        state_name: Name of the state (can have spelling variations)

    Returns:
        Comma-separated list of districts or error message
    """
    # Normalize state name
    state_normalized = state_name.lower().strip()

    # Check for aliases
    if state_normalized in STATE_ALIASES:
        state_normalized = STATE_ALIASES[state_normalized]

    # Try to fetch from API first
    try:
        api_client = DataGovAPIClient()
        # Convert to title case for API (e.g., "Uttar Pradesh")
        state_title = state_normalized.title()
        api_districts = api_client.fetch_districts_for_state(state_title)

        if api_districts and len(api_districts) > 0:
            return f"Districts in {state_title}: {', '.join(api_districts)}"
    except Exception as e:
        print(f"API fetch failed, falling back to hardcoded list: {e}")

    # Fallback to hardcoded list
    # Try exact match
    if state_normalized in INDIAN_STATES:
        districts = INDIAN_STATES[state_normalized]
        return f"Districts in {state_name}: {', '.join(districts)}"

    # Try fuzzy matching
    state_names = list(INDIAN_STATES.keys())
    matches = get_close_matches(state_normalized, state_names, n=1, cutoff=0.6)

    if matches:
        matched_state = matches[0]
        districts = INDIAN_STATES[matched_state]
        return f"Districts in {matched_state.title()} (matched from '{state_name}'): {', '.join(districts)}"

    return f"State '{state_name}' not found. Please check spelling."

@tool("Validate and Correct Location")
def validate_location(state: str, district: str) -> str:
    """
    Validate state and district names and provide corrections if needed.
    
    Args:
        state: State name
        district: District name
    
    Returns:
        Validation result with corrections if applicable
    """
    # Normalize inputs
    state_normalized = state.lower().strip()
    district_normalized = district.lower().strip()
    
    # Check state aliases
    if state_normalized in STATE_ALIASES:
        state_normalized = STATE_ALIASES[state_normalized]
    
    # Validate state
    if state_normalized not in INDIAN_STATES:
        state_matches = get_close_matches(state_normalized, list(INDIAN_STATES.keys()), n=1, cutoff=0.6)
        if state_matches:
            state_normalized = state_matches[0]
        else:
            return f"Invalid state: {state}"
    
    # Validate district
    districts = INDIAN_STATES[state_normalized]
    districts_lower = [d.lower() for d in districts]
    
    if district_normalized in districts_lower:
        idx = districts_lower.index(district_normalized)
        return f"Valid location: {state_normalized.title()}, {districts[idx]}"
    
    # Try fuzzy matching for district
    district_matches = get_close_matches(district_normalized, districts_lower, n=1, cutoff=0.6)
    if district_matches:
        idx = districts_lower.index(district_matches[0])
        return f"Corrected location: {state_normalized.title()}, {districts[idx]} (from '{district}')"
    
    return f"District '{district}' not found in {state_normalized.title()}. Available: {', '.join(districts)}"
