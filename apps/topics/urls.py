from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_topic, name='analyze'),
]