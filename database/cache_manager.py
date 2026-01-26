from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database.db_manager import DatabaseManager
import config

class CacheManager:
    """Manages caching for market prices and location data"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.cache_validity_hours = config.CACHE_VALIDITY_HOURS
    
    def store_market_price(self, state: str, district: str, commodity: str, 
                          modal_price: float, min_price: float, max_price: float,
                          variety: str = None, grade: str = None, market_date: str = None):
        """Store market price data in cache"""
        query = """
            INSERT INTO market_prices 
            (state, district, commodity, modal_price, min_price, max_price, variety, grade, market_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        self.db.execute_insert(query, (
            state, district, commodity, modal_price, min_price, max_price,
            variety, grade, market_date
        ))
    
    def get_cached_price(self, state: str, district: str, commodity: str) -> Optional[Dict]:
        """Retrieve cached price if valid"""
        query = """
            SELECT modal_price, min_price, max_price, variety, grade, market_date, cached_at
            FROM market_prices
            WHERE state = ? AND district = ? AND commodity = ?
            ORDER BY cached_at DESC
            LIMIT 1
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (state, district, commodity))
            row = cursor.fetchone()
            
            if row:
                cached_at = datetime.fromisoformat(row[6])
                validity_threshold = datetime.now() - timedelta(hours=self.cache_validity_hours)
                
                if cached_at > validity_threshold:
                    return {
                        "modal_price": row[0],
                        "min_price": row[1],
                        "max_price": row[2],
                        "variety": row[3],
                        "grade": row[4],
                        "market_date": row[5],
                        "cached_at": row[6]
                    }
            return None
        finally:
            conn.close()
    
    def is_cache_valid(self, state: str, district: str, commodity: str) -> bool:
        """Check if cached data is still valid"""
        cached_data = self.get_cached_price(state, district, commodity)
        return cached_data is not None
    
    def store_district(self, state: str, district: str, normalized_name: str = None):
        """Store district validation data"""
        query = """
            INSERT OR IGNORE INTO districts (state, district, normalized_name)
            VALUES (?, ?, ?)
        """
        
        self.db.execute_insert(query, (state, district, normalized_name or district))
    
    def get_districts_for_state(self, state: str) -> List[str]:
        """Retrieve cached districts for a state"""
        query = """
            SELECT DISTINCT district
            FROM districts
            WHERE state = ?
            ORDER BY district
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (state,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            conn.close()
    
    def cleanup_old_cache(self, days: int = 7):
        """Remove cache entries older than specified days"""
        query = """
            DELETE FROM market_prices
            WHERE cached_at < datetime('now', '-' || ? || ' days')
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (days,))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
