import random
from .interfaces import BaseProvider

class GoogleTrendsProvider(BaseProvider):
    def fetch_score(self, keyword: str) -> int:
        return random.randint(40, 100)

    def fetch_history(self, keyword: str) -> dict:
        return {'labels': ['Lun', 'Mar', 'Mie'], 'values': [10, 20, 30]}