import pytest
from datetime import timedelta
from django.utils import timezone
from freezegun import freeze_time
from apps.topics.models import Topic

@pytest.mark.django_db
class TestTopicModel:

    def test_topic_creation_and_normalization(self):
        '''Verify keyword normalization.'''
        topic = Topic.objects.update_hype_data('  Python  ', 85, {'data': []})
        
        assert topic.name == 'python'
        assert topic.score == 85
        assert topic.history_data == {'data': []}

    def test_timestamped_model_inheritance(self):
        '''Verify created_at and updated_at inherited fields.'''
        topic = Topic.objects.update_hype_data('django', 50, {})
        
        assert topic.created_at is not None
        assert topic.updated_at is not None
        assert isinstance(topic.created_at, timezone.datetime)

    def test_update_existing_topic(self):
        Topic.objects.update_hype_data('htmx', 10, {})
        topic = Topic.objects.update_hype_data('htmx', 95, {'updated': True})
        
        assert Topic.objects.count() == 1
        assert topic.score == 95
        assert topic.history_data == {'updated': True}

    @pytest.mark.parametrize('score, expected_label', [
        (95, 'VIRAL'),
        (90, 'VIRAL'),
        (75, 'NEUTRAL'),
        (50, 'NEUTRAL'),
        (49, 'DEAD ZONE'),
        (0, 'DEAD ZONE'),
    ])
    def test_status_label_thresholds(self, score, expected_label):
        topic = Topic(name='test', score=score)
        assert topic.status_label == expected_label

    def test_is_stale_logic(self):
        initial_time = timezone.now()
        with freeze_time(initial_time):
            topic = Topic.objects.update_hype_data('stale-test', 50, {})
            assert topic.is_stale() is False

        with freeze_time(initial_time + timedelta(hours=23, minutes=59)):
            assert topic.is_stale() is False

        with freeze_time(initial_time + timedelta(hours=25)):
            assert topic.is_stale() is True

    def test_invalid_keyword_raises_error(self):
        with pytest.raises(ValueError, match='The keyword \(name\) cannot be empty.'):
            Topic.objects.update_hype_data('   ', 50, {})

    def test_string_representation(self):
        topic = Topic(name='hypemeter', score=100)
        assert str(topic) == 'hypemeter (100/100)'

    def test_ordering_by_score(self):
        Topic.objects.create(name='low', score=10)
        Topic.objects.create(name='high', score=90)
        Topic.objects.create(name='mid', score=50)
        
        topics = list(Topic.objects.all())
        assert topics[0].name == 'high'
        assert topics[1].name == 'mid'
        assert topics[2].name == 'low'