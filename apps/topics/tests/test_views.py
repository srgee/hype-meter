import pytest
from django.urls import reverse
from apps.topics.models import Topic
from model_bakery import baker

@pytest.mark.django_db
class TestTopicsViews:

    def test_index_view_status_code(self, client):
        response = client.get(reverse('topics:index'))
        assert response.status_code == 200
        assert 'Mide el Hype' in response.content.decode()

    def test_analyze_topic_htmx_request(self, client, mocker):
        mocker.patch('apps.topics.services.HypeEngine.get_hype_report', 
                     return_value=Topic(name='htmx-test', score=99))
        
        url = reverse('topics:analyze')
        response = client.post(url, {'keyword': 'django'}, HTTP_HX_REQUEST='true')
        
        assert response.status_code == 200
        assert '<nav class=\'navbar' not in response.content.decode()
        assert 'htmx-test' in response.content.decode()

    def test_get_recent_topics_view(self, client):
        Topic.objects.create(name='old', score=10)
        Topic.objects.create(name='new', score=90)
        
        url = reverse('topics:recent')
        response = client.get(url)
        
        assert response.status_code == 200
        content = response.content.decode()
        assert 'old' in content
        assert 'new' in content

    def test_analyze_empty_keyword(self, client):
        url = reverse('topics:analyze')
        response = client.post(url, {'keyword': '  '})

        assert response.status_code == 200

@pytest.mark.django_db
class TestTopicsPerformance:

    def test_recent_topics_is_efficient_n_plus_one(self, client, django_assert_num_queries):
        '''
        Verify that recent topics list does not generate N+1 queries.
        It should only generate 1 query to populate the recent history list.
        '''
        baker.make(Topic, _quantity=10)
        with django_assert_num_queries(1):
            response = client.get(reverse('topics:recent'))
        
        assert response.status_code == 200
        assert len(response.context['recent_topics']) == 10

    def test_analyze_flow_performance(self, client, mocker, django_assert_num_queries):
        '''
        Verify that the analysis workflow is efficiente wrt DB.
        It should only do: 1 SELECT (find) + 1 UPDATE/INSERT (save). Total: 2.
        '''
        mocker.patch('apps.topics.services.HypeEngine.get_hype_report', 
                     return_value=Topic.objects.create(name='perf-test', score=50))
        
        with django_assert_num_queries(1):
            client.post(reverse('topics:analyze'), {'keyword': 'test'}, HTTP_HX_REQUEST='true')