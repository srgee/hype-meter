from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .services import HypeEngine


engine = HypeEngine()

def index(request):
    return render(request, 'topics/index.html')

@require_http_methods(['POST'])
def analyze_topic(request):
    keyword = request.POST.get('keyword', '').strip()
    
    if not keyword:
        return render(request, 'partials/hype_result_error.html', {
            'message': 'Por favor, introduce una palabra válida.'
        })

    topic = engine.get_hype_report(keyword)

    if request.headers.get('HX-Request'):
        return render(request, 'partials/hype_result.html', {'topic': topic})

    return render(request, 'topics/index.html', {'topic': topic})