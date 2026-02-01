from django.utils import timezone
from apps.providers.google import GoogleTrendsProvider
from apps.providers.bluesky import BlueskyProvider
from .models import Topic

class HypeEngine:
    '''
    Orchestrator that manages data collection from data providers and implements the scoring logic.
    '''
    
    def __init__(self):
        self.providers = {
            'google': GoogleTrendsProvider(),
            'bluesky': BlueskyProvider()
        }

    def get_hype_report(self, keyword: str) -> Topic:
        '''
        Main entry point. Implments cache-first strategy for the ingested data.
        '''
        keyword = keyword.lower().strip()
        topic = Topic.objects.filter(name=keyword).first()

        if topic and not topic.is_stale():
            return topic

        return self._refresh_topic_data(keyword)

    def _refresh_topic_data(self, keyword: str) -> Topic:
        '''
        Queries available data providers and updates persistance.
        '''
        google_score = self.providers['google'].fetch_score(keyword)
        bluesky_score = self.providers['bluesky'].fetch_score(keyword)
        
        # Calculate weighted average
        final_score = int((google_score * 0.6) + (bluesky_score * 0.4))
        
        combined_history = {
            'google': self.providers['google'].fetch_history(keyword),
            'bluesky': self.providers['bluesky'].fetch_history(keyword),
            'last_refresh': timezone.now().isoformat()
        }

        return Topic.objects.update_hype_data(
            keyword=keyword,
            score=final_score,
            history_data=combined_history
        )