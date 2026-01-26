"""
Simple test script to verify Mandi Saathi setup
"""

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from database.db_manager import DatabaseManager
        from database.session_manager import SessionManager
        from database.cache_manager import CacheManager
        from utils.api_client import DataGovAPIClient
        from utils.price_service import PriceService
        from tools.location_tools import get_districts_for_state, validate_location
        from tools.price_tools import fetch_mandi_prices, normalize_commodity
        from agents.price_discovery_agent import create_price_discovery_agent
        from agents.negotiation_strategist_agent import create_negotiation_strategist_agent
        from agents.communicator_agent import create_communicator_agent
        from agents.crew_manager import MandiSaathiCrew
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_session_manager():
    """Test session manager"""
    print("\nTesting session manager...")
    try:
        from database.db_manager import DatabaseManager
        from database.session_manager import SessionManager
        
        db = DatabaseManager()
        sm = SessionManager(db)
        
        # Generate session ID
        session_id = sm.generate_session_id()
        print(f"  Generated session ID: {session_id}")
        
        # Store test message
        sm.store_chat_history(session_id, "Test user message", "Test assistant response")
        
        # Retrieve
        history = sm.retrieve_chat_history(session_id)
        assert len(history) == 1
        assert history[0]["user"] == "Test user message"
        
        print("✅ Session manager working")
        return True
    except Exception as e:
        print(f"❌ Session manager test failed: {e}")
        return False

def test_tools():
    """Test agent tools"""
    print("\nTesting tools...")
    try:
        from tools.location_tools import get_districts_for_state
        from tools.price_tools import normalize_commodity
        
        # Test location tool
        result = get_districts_for_state("Uttar Pradesh")
        print(f"  Location tool: {result[:50]}...")
        
        # Test commodity normalization
        result = normalize_commodity("tamatar")
        print(f"  Commodity tool: {result}")
        
        print("✅ Tools working")
        return True
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def main():
    print("🌾 Mandi Saathi Setup Verification\n")
    
    tests = [
        test_imports,
        test_database,
        test_session_manager,
        test_tools
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All tests passed! System is ready.")
        print("\nTo start the application:")
        print("  streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("="*50)

if __name__ == "__main__":
    main()
