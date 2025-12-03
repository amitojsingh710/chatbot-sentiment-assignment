import json
from datetime import datetime

class ConversationStorage:
    def __init__(self, file_path="conversation_history.json"):
        self.file_path = file_path
        self.messages = []

    def add_message(self, role: str, text: str, sentiment: str = None):
        self.messages.append({
            "role": role,
            "text": text,
            "sentiment": sentiment,
            "timestamp": str(datetime.now())
        })

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=4)
