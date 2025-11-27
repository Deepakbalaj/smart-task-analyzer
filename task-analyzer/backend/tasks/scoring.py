import datetime
from math import ceil

def parse_date(d):
    if not d:
        return None
    try:
        return datetime.datetime.fromisoformat(d).date()
    except Exception:
        return None

def detect_cycle(tasks):
    visited = {}
    def visit(node):
        if node in visited:
            return visited[node] == 1
        visited[node] = 1
        for dep in tasks.get(node, {}).get('dependencies', []):
            if dep not in tasks:
                continue
            if visit(dep):
                return True
        visited[node] = 2
        return False
    for n in tasks:
        if visit(n):
            return True
    return False

def urgency_score(due_date, today=None):
    today = today or datetime.date.today()
    if not due_date:
        return 10  
    days = (due_date - today).days
    if days < 0:
        return 100 + min(50, -days) 
    if days == 0:
        return 90
    return max(0, 80 - days)

def effort_score(estimated_hours):
    if estimated_hours is None:
        return 10
    try:
        h = float(estimated_hours)
    except Exception:
        return 10
    if h <= 1:
        return 60
    if h <= 3:
        return 40
    if h <= 8:
        return 20
    return 5

def importance_score(importance):
    try:
        i = float(importance)
    except Exception:
        i = 5
    return max(0, min(10, i)) * 10

def dependency_score(task_id, task_map):
    count = 0
    for t in task_map.values():
        if task_id in t.get('dependencies', []):
            count += 1
    return min(50, count * 15)

def score_task(task, task_map, today=None):
    today = today or datetime.date.today()
    title = task.get('title', '<untitled>')
    due = parse_date(task.get('due_date'))
    urg = urgency_score(due, today)
    imp = importance_score(task.get('importance'))
    eff = effort_score(task.get('estimated_hours'))
    dep = dependency_score(task.get('id') or title, task_map)
    w_urg = 0.35
    w_imp = 0.35
    w_eff = 0.15
    w_dep = 0.15
    raw = w_urg * urg + w_imp * imp + w_eff * eff + w_dep * dep
    return round(max(0, min(100, raw)), 2)

def analyze_tasks(task_list, today=None):
    task_map = {}
    for i, t in enumerate(task_list):
        key = t.get('id') or f'idx-{i}'
        task_map[key] = dict(t)
        task_map[key]['_key'] = key
    has_cycle = detect_cycle(task_map)
    scores = []
    for k, t in task_map.items():
        t_copy = dict(t)
        t_copy['id'] = k
        try:
            t_copy['score'] = score_task(t_copy, task_map, today)
        except Exception:
            t_copy['score'] = 0
        scores.append(t_copy)
    scores_sorted = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)
    return {'has_cycle': has_cycle, 'tasks': scores_sorted}
