import random
from .interfaces import BaseProvider

class BlueskyProvider(BaseProvider):
    def fetch_score(self, keyword: str) -> int:
        return random.randint(10, 80)

    def fetch_history(self, keyword: str) -> dict:
        return {'mentions': random.randint(100, 1000)}