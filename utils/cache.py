import json
import os
from instagrapi import Client

class SessionManager:
    def __init__(self, client: Client, session_path="session.json"):
        self.client = client
        self.session_path = session_path

    def save_session(self):
        session_data = {
            "username": self.client.username,
            "settings": self.client.settings,
            "authorization_data": self.client.authorization_data
        }
        with open(self.session_path, "w") as f:
            json.dump(session_data, f, indent=2)

    def load_session(self):
        if os.path.exists(self.session_path):
            with open(self.session_path, "r") as f:
                data = json.load(f)
            self.client.settings = data["settings"]
            self.client.authorization_data = data["authorization_data"]
            return True
        return False