from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.requests = deque()

    def can_request(self) -> bool:
        current_time = datetime.now()
        self._clean_requests(current_time)
        return len(self.requests) < self.limit

    def add_request(self):
        current_time = datetime.now()
        self.requests.append(current_time)

    def _clean_requests(self, current_time: datetime):
        cutoff = current_time - timedelta(seconds=self.window)
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()