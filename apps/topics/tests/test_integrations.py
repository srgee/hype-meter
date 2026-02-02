import pytest
from apps.topics.services import HypeEngine
from apps.topics.models import Topic
from apps.providers.bluesky import BlueskyProvider

@pytest.mark.django_db
class TestHypeEngineIntegration:

    @pytest.fixture
    def engine(self):
        return HypeEngine()

    def test_full_refresh_flow(self, mocker, engine):

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

        topic = engine.get_hype_report('python')


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

    def test_google_provider_error_handling(self, mocker, engine):
        mocker.patch('apps.providers.google.GoogleTrendsProvider.fetch_score', side_effect=Exception('Timeout'))
        mocker.patch('apps.providers.social.SocialProvider.fetch_score', return_value=50)
        
        # Google devuelve 0 por el exception handling interno, social da 50.
        # (0 * 0.6) + (50 * 0.4) = 20
        topic = engine.get_hype_report('test-error')
        assert topic.score == 20

    def test_bluesky_requests_parsing(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.json.return_value = {'posts': [{'id': 1}, {'id': 2}]}
        mock_resp.status_code = 200
        mocker.patch('requests.get', return_value=mock_resp)

        provider = BlueskyProvider()
        score = provider.fetch_score('python')
        
        # Según nuestra lógica: (2/40) * 100 = 5
        assert score == 5

    def test_engine_weighted_calculation(self, mocker, engine):
        mocker.patch('apps.providers.google.GoogleTrendsProvider.fetch_score', return_value=100)
        mocker.patch('apps.providers.social.SocialProvider.fetch_score', return_value=50)
        mocker.patch('apps.providers.google.GoogleTrendsProvider.fetch_history', return_value={'data': 1})
        mocker.patch('apps.providers.social.SocialProvider.fetch_history', return_value={})

        topic = engine.get_hype_report('test-calc')
        
        # (100 * 0.6) + (50 * 0.4) = 60 + 20 = 80
        assert topic.score == 80