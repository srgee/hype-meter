from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .services import HypeEngine
from .models import Topic


engine = HypeEngine()

def index(request):
    return render(request, 'topics/index.html')

@require_http_methods(['POST'])
def analyze_topic(request):
    keyword = request.POST.get('keyword', '').strip()
    
    if not keyword:
        return render(request, 'partials/hype_result_error.html', {
            'message': 'Please enter a valid word.'
        })

    topic = engine.get_hype_report(keyword)

    if request.headers.get('HX-Request'):
        return render(request, 'partials/hype_result.html', {'topic': topic})

    return render(request, 'topics/index.html', {'topic': topic})

def get_recent_topics(request):
    '''Devuelve una lista con los 10 temas más recientes basados en updated_at'''
    recent = Topic.objects.all().order_by('-updated_at')[:10]
    return render(request, 'partials/recent_list.html', {'recent_topics': recent})