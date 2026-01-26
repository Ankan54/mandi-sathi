from crewai.tools import tool
from difflib import get_close_matches
from database.db_manager import DatabaseManager
from utils.price_service import PriceService

# Commodity name mappings (Hindi/Hinglish to English)
COMMODITY_MAPPINGS = {
    "tamatar": "Tomato",
    "aalu": "Potato",
    "alu": "Potato",
    "pyaz": "Onion",
    "onion": "Onion",
    "tomato": "Tomato",
    "potato": "Potato",
    "gobi": "Cauliflower",
    "cauliflower": "Cauliflower",
    "bhindi": "Lady Finger",
    "ladyfinger": "Lady Finger",
    "palak": "Spinach",
    "spinach": "Spinach",
    "dhaniya": "Coriander",
    "coriander": "Coriander",
    "mirch": "Chilli",
    "chilli": "Chilli",
    "chili": "Chilli",
    "baigan": "Brinjal",
    "brinjal": "Brinjal",
    "eggplant": "Brinjal",
    "gajar": "Carrot",
    "carrot": "Carrot",
    "matar": "Peas",
    "peas": "Peas",
    "sarson": "Mustard",
    "mustard": "Mustard",
    "gehun": "Wheat",
    "wheat": "Wheat",
    "chawal": "Rice",
    "rice": "Rice",
    "dhan": "Paddy",
    "paddy": "Paddy",
}

# Initialize database and price service
db_manager = DatabaseManager()
price_service = PriceService(db_manager)

def normalize_commodity_name(commodity: str) -> str:
    """Normalize commodity name to standard format"""
    commodity_lower = commodity.lower().strip()
    
    # Direct mapping
    if commodity_lower in COMMODITY_MAPPINGS:
        return COMMODITY_MAPPINGS[commodity_lower]
    
    # Fuzzy matching
    matches = get_close_matches(commodity_lower, COMMODITY_MAPPINGS.keys(), n=1, cutoff=0.7)
    if matches:
        return COMMODITY_MAPPINGS[matches[0]]
    
    # Return capitalized version if no match
    return commodity.title()

@tool("Fetch Mandi Prices")
def fetch_mandi_prices(state: str, district: str, commodity: str) -> str:
    """
    Fetch current market prices for a commodity in a specific mandi.
    Returns modal price, min/max range, and prices from neighboring districts.
    
    Args:
        state: State name
        district: District name
        commodity: Commodity name (can be in Hindi/Hinglish)
    
    Returns:
        Formatted price information or error message
    """
    # Normalize commodity name
    normalized_commodity = normalize_commodity_name(commodity)
    
    # Fetch prices
    price_data = price_service.get_market_prices(state, district, normalized_commodity)
    
    if not price_data:
        return f"No price data available for {normalized_commodity} in {district}, {state}. Try nearby markets."
    
    data = price_data["data"]
    source = price_data["source"]
    
    # Format response
    response = f"""
Price Information for {normalized_commodity} in {district}, {state}:
- Modal Price: ₹{data['modal_price']:.2f} per quintal
- Price Range: ₹{data['min_price']:.2f} - ₹{data['max_price']:.2f}
- Variety: {data.get('variety', 'Not specified')}
- Grade: {data.get('grade', 'Not specified')}
- Date: {data.get('market_date', 'Recent')}
- Source: {source}
"""
    
    # Add neighboring prices if available
    if price_data.get("neighboring_prices"):
        response += "\nPrices in Nearby Districts:\n"
        for neighbor in price_data["neighboring_prices"]:
            response += f"- {neighbor['district']}: ₹{neighbor['modal_price']:.2f} (Modal)\n"
    
    # Add note if fallback
    if price_data.get("note"):
        response += f"\nNote: {price_data['note']}\n"
    
    return response

@tool("Normalize Commodity Name")
def normalize_commodity(commodity: str) -> str:
    """
    Normalize commodity name from Hindi/Hinglish to standard English name.
    
    Args:
        commodity: Commodity name in any language
    
    Returns:
        Standardized commodity name
    """
    normalized = normalize_commodity_name(commodity)
    return f"Normalized '{commodity}' to '{normalized}'"
