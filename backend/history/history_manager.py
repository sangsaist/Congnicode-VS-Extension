import json
import os

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "user_history.json")

class HistoryManager:
    def __init__(self):
        self._ensure_history_file()

    def _ensure_history_file(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w") as f:
                json.dump({}, f)

    def get_user_history(self, user_id):
        if not user_id:
            return []
        
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                return data.get(str(user_id), [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_to_history(self, user_id, pattern, complexity):
        if not user_id:
            return
            
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        user_records = data.get(str(user_id), [])
        user_records.append({
            "pattern": pattern,
            "complexity": complexity
        })
        
        # Keep only last 5 records for context
        data[str(user_id)] = user_records[-5:]

        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
