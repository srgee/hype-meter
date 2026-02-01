import pytest
from apps.topics.services import HypeEngine
from apps.topics.models import Topic

@pytest.mark.django_db
class TestHypeEngineIntegration:

    def setup_method(self):
        self.engine = HypeEngine()

    def test_full_refresh_flow(self, mocker):

        mock_google = mocker.patch(
            'apps.providers.google.GoogleTrendsProvider.fetch_score', 
            return_value=100
        )
        mock_bluesky = mocker.patch(
            'apps.providers.bluesky.BlueskyProvider.fetch_score', 
            return_value=50
        )
        
        mocker.patch(
            'apps.providers.google.GoogleTrendsProvider.fetch_history', 
            return_value={'labels': ['A'], 'values': [1]}
        )
        mocker.patch(
            'apps.providers.bluesky.BlueskyProvider.fetch_history', 
            return_value={'mentions': 5}
        )

        topic = self.engine.get_hype_report('python')


        assert Topic.objects.count() == 1
        assert topic.name == 'python'
        assert topic.score == 80  # (100 * 0.6) + (50 * 0.4)
        
        mock_google.assert_called_once_with('python')
        mock_bluesky.assert_called_once_with('python')

    def test_engine_handles_provider_failure(self, mocker):
        mocker.patch(
            'apps.providers.google.GoogleTrendsProvider.fetch_score', 
            side_effect=Exception('API Down')
        )
        
        with pytest.raises(Exception, match='API Down'):
            self.engine.get_hype_report('python')