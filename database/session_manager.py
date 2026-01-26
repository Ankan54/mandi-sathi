import json
from datetime import datetime
from typing import List, Dict, Optional
from database.db_manager import DatabaseManager

class SessionManager:
    """Manages chat sessions and history"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def generate_session_id(self) -> str:
        """Generate unique session ID based on timestamp with milliseconds"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def store_chat_history(self, session_id: str, user_message: str, assistant_response: str) -> None:
        """Store chat interaction with JSON format"""
        conn = self.db.get_connection()
        try:
            # Check if session exists
            cursor = conn.cursor()
            cursor.execute("SELECT session_id FROM chat_sessions WHERE session_id = ?", (session_id,))
            session_exists = cursor.fetchone()
            
            if not session_exists:
                # Create new session
                cursor.execute(
                    """INSERT INTO chat_sessions (session_id, first_message, message_count)
                       VALUES (?, ?, 1)""",
                    (session_id, user_message)
                )
            else:
                # Update existing session
                cursor.execute(
                    """UPDATE chat_sessions 
                       SET last_updated = CURRENT_TIMESTAMP,
                           message_count = message_count + 1
                       WHERE session_id = ?""",
                    (session_id,)
                )
            
            # Store message with JSON format
            chat_data = json.dumps({
                "user": user_message,
                "assistant": assistant_response
            })
            
            cursor.execute(
                """INSERT INTO chat_messages (session_id, user_message, assistant_response, chat_data)
                   VALUES (?, ?, ?, ?)""",
                (session_id, user_message, assistant_response, chat_data)
            )
            
            conn.commit()
        finally:
            conn.close()
    
    def retrieve_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieve all messages for a session"""
        query = """
            SELECT user_message, assistant_response, created_at
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY created_at ASC
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (session_id,))
            rows = cursor.fetchall()
            
            return [
                {
                    "user": row[0],
                    "assistant": row[1],
                    "timestamp": row[2]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_all_sessions(self) -> List[Dict[str, any]]:
        """Get all chat sessions with summary info"""
        query = """
            SELECT session_id, created_at, last_updated, first_message, message_count
            FROM chat_sessions
            ORDER BY last_updated DESC
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                {
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_updated": row[2],
                    "first_message": row[3],
                    "message_count": row[4]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, any]]:
        """Get summary info for a specific session"""
        query = """
            SELECT session_id, created_at, last_updated, first_message, message_count
            FROM chat_sessions
            WHERE session_id = ?
        """
        
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (session_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_updated": row[2],
                    "first_message": row[3],
                    "message_count": row[4]
                }
            return None
        finally:
            conn.close()
