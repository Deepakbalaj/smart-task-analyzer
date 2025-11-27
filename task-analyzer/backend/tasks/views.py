import json
from django.http import JsonResponse, HttpResponseBadRequest
from . import scoring
from datetime import date

def _load_json(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except Exception:
        return None

def analyze_tasks(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(json.dumps({'error': 'POST required'}), content_type='application/json')
    data = _load_json(request)
    if not isinstance(data, list):
        return HttpResponseBadRequest(json.dumps({'error': 'expected a JSON array of tasks'}), content_type='application/json')
    result = analyze_tasks_internal(data)
    return JsonResponse(result, safe=False)

def analyze_tasks_internal(task_list):
    # call the scoring module's analyze_tasks to avoid name shadowing with the view
    return scoring.analyze_tasks(task_list, today=date.today())

def suggest_tasks(request):
    if request.method == 'GET':
        return HttpResponseBadRequest(json.dumps({'error': 'GET requires tasks as query? Use POST to /analyze/ instead.'}), content_type='application/json')
    if request.method == 'POST':
        data = _load_json(request)
        if not isinstance(data, list):
            return HttpResponseBadRequest(json.dumps({'error': 'expected a JSON array of tasks'}), content_type='application/json')
        analysis = analyze_tasks_internal(data)
        top3 = analysis['tasks'][:3]
        for t in top3:
            t['explanation'] = f"Score {t.get('score')} -> urgent/importance/effort balance."
        return JsonResponse({'suggestions': top3})
