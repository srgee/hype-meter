import random
from .interfaces import BaseProvider
from apps.core.decorators import trace_provider_call

class BlueskyProvider(BaseProvider):
    @trace_provider_call
    def fetch_score(self, keyword: str) -> int:
        return random.randint(10, 80)

    @trace_provider_call
    def fetch_history(self, keyword: str) -> dict:
        return {'mentions': random.randint(100, 1000)}