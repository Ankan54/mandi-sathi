from crewai import Agent
from tools.location_tools import get_districts_for_state, validate_location
from tools.price_tools import fetch_mandi_prices, normalize_commodity
import config

def create_price_discovery_agent():
    """Create and configure the Price Discovery Agent"""
    
    return Agent(
        role="Price Discovery Specialist",
        goal="""Extract location (state, district) and commodity details from farmer's message,
        validate the information, and fetch current market prices from data.gov.in.
        Handle spelling variations, Hindi/Hinglish input, and informal language.""",
        backstory="""You are an expert in Indian agricultural markets with deep knowledge of 
        mandi systems across all states. You understand farmer's language - whether they speak 
        in Hindi, English, or Hinglish. You can identify locations even with spelling mistakes 
        (like 'Balia' for 'Ballia') and commodities in local languages (like 'tamatar' for tomato).
        
        Your expertise includes:
        - Understanding informal farmer communication
        - Correcting spelling variations in location names
        - Translating Hindi/Hinglish commodity names to standard English
        - Fetching accurate, up-to-date market prices
        - Providing comprehensive price data including nearby markets
        
        You always validate locations against official records and normalize commodity names 
        before fetching prices.""",
        tools=[
            get_districts_for_state,
            validate_location,
            fetch_mandi_prices,
            normalize_commodity
        ],
        verbose=True,
        allow_delegation=False,
        llm=config.AGENT_MODEL
    )
