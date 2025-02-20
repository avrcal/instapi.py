import asyncio
import json
from instagrapi import Client
from instagrapi.exceptions import ClientError
from .models import Message, User
from .rest import RESTClient
from utils.cache import SessionManager
from utils.security import RateLimiter
from utils.helpers import HelperFunctions

class InstagramClient:
    def __init__(self, config_path="config/config.json"):
        self.config = json.load(open(config_path))
        self.client = Client()
        self.session = SessionManager(self.client)
        self.rest = RESTClient(self.client)
        self.direct_rate_limiter = RateLimiter(
            self.config["rate_limits"]["direct_messages"]["limit"],
            self.config["rate_limits"]["direct_messages"]["window"]
        )
        self.media_rate_limiter = RateLimiter(
            self.config["rate_limits"]["media_uploads"]["limit"],
            self.config["rate_limits"]["media_uploads"]["window"]
        )
        self.listeners = {
            "message": [],
            "media_upload": [],
            "follow": []
        }
        self.logged_in = False

    async def login(self, force=False):
        if not force and self.session.load_session():
            self.logged_in = True
            return True
        try:
            self.client.login(
                self.config["username"],
                self.config["password"]
            )
            self.logged_in = True
            self.session.save_session()
            return True
        except ClientError as e:
            print(f"[!] Login failed: {e}")
            return False

    async def send_message(self, recipient_id: str, text: str):
        if not self.direct_rate_limiter.can_request():
            wait_time = self.direct_rate_limiter.window
            print(f"[!] Rate-limited. Wait for {wait_time} seconds.")
            return False
        try:
            self.client.direct_send(text=text, user_ids=[recipient_id])
            self.direct_rate_limiter.add_request()
            return True
        except ClientError as e:
            print(f"[!] Failed to send message: {e}")
            return False

    async def send_media(self, recipient_id: str, media_path: str, caption=""):
        if not HelperFunctions.validate_media_path(media_path, self.config["media_upload"]["max_size"]):
            print("[!] Invalid media path or size exceeds limit")
            return False
        if not self.media_rate_limiter.can_request():
            print("[!] Rate-limited for media uploads")
            return False
        try:
            media = self.client.photo_upload(media_path, caption)
            self.client.direct_send(media.pk, [recipient_id], "photo")
            self.media_rate_limiter.add_request()
            return True
        except ClientError as e:
            print(f"[!] Failed to send media: {e}")
            return False

    async def handle_events(self):
        while True:
            await asyncio.sleep(self.config["poll_interval"])
            if not self.logged_in:
                if await self.login():
                    await self._check_unseen_events()
                continue
            await self._check_unseen_messages()

    async def _check_unseen_messages(self):
        inbox = self.client.direct_inbox()
        for thread in inbox.threads:
            for item in thread.items:
                message = Message(item, thread)
                for listener in self.listeners.get("message", []):
                    await listener(message)

    def event(self, func):
        event_name = func.__name__
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(func)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.handle_events())