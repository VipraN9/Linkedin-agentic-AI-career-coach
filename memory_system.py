import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
import config

class ProfileMemorySystem:
    def __init__(self):
        self.memory_saver = MemorySaver()
        self.memory_file = "user_memory.json"
        self.session_memory = {}
        self.persistent_memory = self._load_persistent_memory()
        
    def _load_persistent_memory(self) -> Dict:
        """Load persistent memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading persistent memory: {e}")
        return {}
    
    def _save_persistent_memory(self):
        """Save persistent memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.persistent_memory, f, indent=2)
        except Exception as e:
            print(f"Error saving persistent memory: {e}")
    
    def get_user_session(self, user_id: str) -> Dict:
        """Get or create user session memory"""
        if user_id not in self.session_memory:
            self.session_memory[user_id] = {
                "session_start": datetime.now().isoformat(),
                "messages": [],
                "profile_data": None,
                "current_context": {},
                "interaction_count": 0
            }
        return self.session_memory[user_id]
    
    def get_user_persistent(self, user_id: str) -> Dict:
        """Get or create user persistent memory"""
        if user_id not in self.persistent_memory:
            self.persistent_memory[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "profile_history": [],
                "career_goals": [],
                "job_preferences": [],
                "skill_gaps": [],
                "interaction_history": [],
                "preferences": {}
            }
            self._save_persistent_memory()
        return self.persistent_memory[user_id]
    
    def add_message(self, user_id: str, message: str, sender: str = "user"):
        """Add message to session memory"""
        session = self.get_user_session(user_id)
        persistent = self.get_user_persistent(user_id)
        
        message_data = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "message": message
        }
        
        session["messages"].append(message_data)
        session["interaction_count"] += 1
        
        # Keep only recent messages in session
        if len(session["messages"]) > config.MAX_MEMORY_SIZE:
            session["messages"] = session["messages"][-config.MAX_MEMORY_SIZE:]
        
        # Add to persistent history
        persistent["interaction_history"].append(message_data)
        persistent["last_updated"] = datetime.now().isoformat()
        
        # Keep only recent history in persistent
        if len(persistent["interaction_history"]) > config.MAX_MEMORY_SIZE * 2:
            persistent["interaction_history"] = persistent["interaction_history"][-config.MAX_MEMORY_SIZE * 2:]
        
        self._save_persistent_memory()
    
    def update_profile_data(self, user_id: str, profile_data: Dict):
        """Update user's profile data in memory"""
        session = self.get_user_session(user_id)
        persistent = self.get_user_persistent(user_id)
        
        session["profile_data"] = profile_data
        
        # Add to profile history
        profile_entry = {
            "timestamp": datetime.now().isoformat(),
            "profile_data": profile_data
        }
        persistent["profile_history"].append(profile_entry)
        
        # Keep only recent profile history
        if len(persistent["profile_history"]) > 10:
            persistent["profile_history"] = persistent["profile_history"][-10:]
        
        persistent["last_updated"] = datetime.now().isoformat()
        self._save_persistent_memory()
    
    def update_career_goals(self, user_id: str, goals: List[str]):
        """Update user's career goals"""
        persistent = self.get_user_persistent(user_id)
        persistent["career_goals"] = goals
        persistent["last_updated"] = datetime.now().isoformat()
        self._save_persistent_memory()
    
    def update_job_preferences(self, user_id: str, preferences: Dict):
        """Update user's job preferences"""
        persistent = self.get_user_persistent(user_id)
        persistent["job_preferences"] = preferences
        persistent["last_updated"] = datetime.now().isoformat()
        self._save_persistent_memory()
    
    def update_skill_gaps(self, user_id: str, skill_gaps: List[Dict]):
        """Update identified skill gaps"""
        persistent = self.get_user_persistent(user_id)
        persistent["skill_gaps"] = skill_gaps
        persistent["last_updated"] = datetime.now().isoformat()
        self._save_persistent_memory()
    
    def get_conversation_context(self, user_id: str, max_messages: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        session = self.get_user_session(user_id)
        return session["messages"][-max_messages:] if session["messages"] else []
    
    def get_profile_context(self, user_id: str) -> Optional[Dict]:
        """Get current profile context"""
        session = self.get_user_session(user_id)
        return session["profile_data"]
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences and history"""
        persistent = self.get_user_persistent(user_id)
        return {
            "career_goals": persistent.get("career_goals", []),
            "job_preferences": persistent.get("job_preferences", {}),
            "skill_gaps": persistent.get("skill_gaps", []),
            "preferences": persistent.get("preferences", {})
        }
    
    def clear_session(self, user_id: str):
        """Clear user session memory"""
        if user_id in self.session_memory:
            del self.session_memory[user_id]
    
    def get_memory_summary(self, user_id: str) -> Dict:
        """Get a summary of user's memory"""
        session = self.get_user_session(user_id)
        persistent = self.get_user_persistent(user_id)
        
        return {
            "session_info": {
                "session_start": session.get("session_start"),
                "interaction_count": session.get("interaction_count", 0),
                "has_profile": session.get("profile_data") is not None
            },
            "persistent_info": {
                "created_at": persistent.get("created_at"),
                "last_updated": persistent.get("last_updated"),
                "profile_history_count": len(persistent.get("profile_history", [])),
                "career_goals": persistent.get("career_goals", []),
                "skill_gaps_count": len(persistent.get("skill_gaps", []))
            }
        }
    
    def cleanup_old_sessions(self):
        """Clean up old session data"""
        current_time = datetime.now()
        expired_sessions = []
        
        for user_id, session in self.session_memory.items():
            session_start = datetime.fromisoformat(session["session_start"])
            if current_time - session_start > timedelta(seconds=config.MEMORY_TTL):
                expired_sessions.append(user_id)
        
        for user_id in expired_sessions:
            self.clear_session(user_id)
