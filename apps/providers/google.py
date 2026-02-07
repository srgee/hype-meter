import random
from .interfaces import BaseProvider
from apps.core.decorators import trace_provider_call

class GoogleTrendsProvider(BaseProvider):
    @trace_provider_call
    def fetch_score(self, keyword: str) -> int:
        return random.randint(40, 100)

    @trace_provider_call
    def fetch_history(self, keyword: str) -> dict:
        return {'labels': ['Lun', 'Mar', 'Mie'], 'values': [10, 20, 30]}