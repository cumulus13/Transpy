#!/usr/bin/env python3
# History management for Transpy - No dependencies!

import os
import json
import datetime

class HistoryManager:
    """Simple history management without external dependencies"""
    
    def __init__(self, history_file=None):
        if history_file is None:
            history_file = os.path.expanduser("~/.transpy_history.json")
        self.history_file = history_file
        self.max_entries = 100
    
    def save_entry(self, original, translated, src_lang, dest_lang, confidence=0.0):
        """Save translation to history"""
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'original': original,
            'translated': translated,
            'from_lang': src_lang,
            'to_lang': dest_lang,
            'confidence': confidence
        }
        
        try:
            # Load existing history
            history = self.load_history()
            
            # Add new entry and keep last N
            history.append(entry)
            history = history[-self.max_entries:]
            
            # Save back
            self._save_history(history)
            return True
        except Exception as e:
            print("Transpy: History save failed - {}".format(e))
            return False
    
    def load_history(self):
        """Load history from file"""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    return json.loads(content)
                return []
        except Exception as e:
            print("Transpy: Failed to load history - {}".format(e))
            return []
    
    def _save_history(self, history):
        """Save history to file"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(history, ensure_ascii=False, indent=2))
        except Exception as e:
            print("Transpy: Failed to save history - {}".format(e))
    
    def clear_history(self):
        """Clear translation history"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            return True
        return False
    
    def get_recent_entries(self, limit=10):
        """Get recent history entries"""
        history = self.load_history()
        return history[-limit:]


# Test function
if __name__ == "__main__":
    history_mgr = HistoryManager()
    
    # Test save
    success = history_mgr.save_entry("Hello", "Halo", "en", "id", 0.9)
    print("History save test: {}".format(success))
    
    # Test load
    entries = history_mgr.get_recent_entries(5)
    print("History load test: {} entries".format(len(entries)))