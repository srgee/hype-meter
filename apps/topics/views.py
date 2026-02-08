from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .services import HypeEngine
from .models import Topic
import logging

logger = logging.getLogger("apps.topics")

engine = HypeEngine()

def index(request):
    return render(request, 'topics/index.html')

@require_http_methods(['POST'])
def analyze_topic(request):
    keyword = request.POST.get('keyword', '').strip()
    
    if not keyword:
        logger.info("keyword_search_rejected", extra={
            "reason": "empty_keyword",
            "user_agent": request.META.get('HTTP_USER_AGENT', 'unknown'),
            "is_htmx": request.headers.get('HX-Request') is not None
        })
        return render(request, 'partials/hype_result_error.html', {
            'message': 'Please enter a valid word.'
        })

    topic = engine.get_hype_report(keyword)
    logger.info("topic__success", extra={
        "topic": topic.name,
    })

    if request.headers.get('HX-Request'):
        return render(request, 'partials/hype_result.html', {'topic': topic})

    return render(request, 'topics/index.html', {'topic': topic})

def get_recent_topics(request):
    recent = Topic.objects.all().order_by('-updated_at')[:10]
    return render(request, 'partials/recent_list.html', {'recent_topics': recent})