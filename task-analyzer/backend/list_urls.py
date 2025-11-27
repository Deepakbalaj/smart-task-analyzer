import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_analyzer.settings')
import django
django.setup()
from django.urls import get_resolver

def walk(patterns, prefix=''):
    for p in patterns:
        try:
            pat = p.pattern._route
        except Exception:
            pat = str(p.pattern)
        name = getattr(p, 'name', None)
        cb = getattr(p, 'callback', None)
        print(prefix + pat, 'name=', name, 'callback=', getattr(cb, '__name__', repr(cb)))
        if hasattr(p, 'url_patterns') and p.url_patterns:
            walk(p.url_patterns, prefix + pat)

res = get_resolver(None)
walk(res.url_patterns)
