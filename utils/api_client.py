import requests
import time
from typing import Dict, List, Optional
import config

class DataGovAPIClient:
    """Client for data.gov.in API to fetch mandi prices"""
    
    def __init__(self):
        self.base_url = config.DATA_GOV_API_URL
        self.resource_id = config.DATA_GOV_RESOURCE_ID
        self.api_key = config.DATA_GOV_API_KEY
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def _make_request(self, params: Dict, retry_count: int = 0) -> Optional[Dict]:
        """Make API request with retry logic"""
        try:
            # Add API key and format to params
            request_params = {
                "api-key": self.api_key,
                "format": "json",
                **params
            }

            response = requests.get(
                f"{self.base_url}/{self.resource_id}",
                params=request_params,
                timeout=15
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if retry_count < self.max_retries:
                # Exponential backoff
                wait_time = self.retry_delay * (2 ** retry_count)
                time.sleep(wait_time)
                return self._make_request(params, retry_count + 1)
            else:
                print(f"API request failed after {self.max_retries} retries: {e}")
                return None
    
    def fetch_mandi_prices(self, state: str, district: str, commodity: str,
                          limit: int = 100) -> Optional[List[Dict]]:
        """Fetch mandi prices for given location and commodity"""
        params = {
            "filters[State]": state,
            "filters[District]": district,
            "filters[Commodity]": commodity,
            "limit": limit,
            "sort[Arrival_Date]": "desc"
        }
        
        response_data = self._make_request(params)
        
        if response_data and "records" in response_data:
            return response_data["records"]
        return None
    
    def fetch_prices_by_state_commodity(self, state: str, commodity: str,
                                       limit: int = 100) -> Optional[List[Dict]]:
        """Fetch prices for a commodity across all districts in a state"""
        params = {
            "filters[State]": state,
            "filters[Commodity]": commodity,
            "limit": limit,
            "sort[Arrival_Date]": "desc"
        }
        
        response_data = self._make_request(params)
        
        if response_data and "records" in response_data:
            return response_data["records"]
        return None
    
    def fetch_districts_for_state(self, state: str) -> Optional[List[str]]:
        """Fetch all districts for a given state from data.gov.in API"""
        params = {
            "filters[State]": state,
            "aggr[District][terms][field]": "District",
            "aggr[District][terms][size]": 1000,
            "aggr_show": 1
        }

        response_data = self._make_request(params)

        if response_data and "records" in response_data:
            # Extract unique district names from records
            districts = list(set([record.get("District", "") for record in response_data["records"] if record.get("District")]))
            return sorted(districts)
        return None

    def parse_price_record(self, record: Dict) -> Dict:
        """Parse API response record into standardized format"""
        try:
            return {
                "state": record.get("State", ""),
                "district": record.get("District", ""),
                "market": record.get("Market", ""),
                "commodity": record.get("Commodity", ""),
                "variety": record.get("Variety", ""),
                "grade": record.get("Grade", ""),
                "modal_price": float(record.get("Modal_Price", 0)),
                "min_price": float(record.get("Min_Price", 0)),
                "max_price": float(record.get("Max_Price", 0)),
                "price_date": record.get("Arrival_Date", "")
            }
        except (ValueError, TypeError) as e:
            print(f"Error parsing price record: {e}")
            return None
