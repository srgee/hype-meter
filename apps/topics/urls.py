from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_topic, name='analyze'),
    path('recent/', views.get_recent_topics, name='recent'),
]