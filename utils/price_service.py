from typing import Dict, List, Optional
from utils.api_client import DataGovAPIClient
from database.cache_manager import CacheManager
from database.db_manager import DatabaseManager

class PriceService:
    """Service layer for fetching prices with caching and fallback"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.api_client = DataGovAPIClient()
        self.cache_manager = CacheManager(db_manager)
    
    def get_market_prices(self, state: str, district: str, commodity: str) -> Optional[Dict]:
        """Get market prices with caching and fallback"""
        # Try cache first
        cached_price = self.cache_manager.get_cached_price(state, district, commodity)
        if cached_price:
            return {
                "source": "cache",
                "data": cached_price,
                "neighboring_prices": []
            }
        
        # Try API
        try:
            api_records = self.api_client.fetch_mandi_prices(state, district, commodity)
            
            if api_records and len(api_records) > 0:
                # Parse and cache the first record
                parsed = self.api_client.parse_price_record(api_records[0])
                
                if parsed:
                    # Store in cache
                    self.cache_manager.store_market_price(
                        state=parsed["state"],
                        district=parsed["district"],
                        commodity=parsed["commodity"],
                        modal_price=parsed["modal_price"],
                        min_price=parsed["min_price"],
                        max_price=parsed["max_price"],
                        variety=parsed["variety"],
                        grade=parsed["grade"],
                        market_date=parsed["price_date"]
                    )
                    
                    # Get neighboring district prices
                    neighboring = self._get_neighboring_prices(state, commodity, district)
                    
                    return {
                        "source": "api",
                        "data": parsed,
                        "neighboring_prices": neighboring
                    }
        except Exception as e:
            print(f"Error fetching from API: {e}")
        
        # Fallback: Try to get prices from nearby districts
        fallback_data = self._fallback_to_nearby_markets(state, commodity, district)
        if fallback_data:
            return fallback_data
        
        return None
    
    def _get_neighboring_prices(self, state: str, commodity: str, 
                               exclude_district: str = None) -> List[Dict]:
        """Get prices from neighboring districts"""
        try:
            records = self.api_client.fetch_prices_by_state_commodity(state, commodity, limit=5)
            
            if not records:
                return []
            
            neighboring = []
            for record in records:
                if exclude_district and record.get("district") == exclude_district:
                    continue
                
                parsed = self.api_client.parse_price_record(record)
                if parsed:
                    neighboring.append(parsed)
            
            return neighboring[:3]  # Return top 3
        except Exception as e:
            print(f"Error fetching neighboring prices: {e}")
            return []
    
    def _fallback_to_nearby_markets(self, state: str, commodity: str, 
                                   original_district: str) -> Optional[Dict]:
        """Fallback to nearby markets when primary location unavailable"""
        try:
            # Try to get any prices from the state
            records = self.api_client.fetch_prices_by_state_commodity(state, commodity, limit=10)
            
            if records and len(records) > 0:
                parsed = self.api_client.parse_price_record(records[0])
                
                if parsed:
                    return {
                        "source": "fallback",
                        "data": parsed,
                        "neighboring_prices": [],
                        "note": f"Data from {parsed['district']} (nearby market) as {original_district} data unavailable"
                    }
        except Exception as e:
            print(f"Fallback failed: {e}")
        
        return None
    
    def validate_api_response(self, records: List[Dict]) -> bool:
        """Validate API response completeness"""
        if not records or len(records) == 0:
            return False
        
        required_fields = ["state", "district", "commodity", "modal_price"]
        
        for record in records:
            for field in required_fields:
                if field not in record or not record[field]:
                    return False
        
        return True
