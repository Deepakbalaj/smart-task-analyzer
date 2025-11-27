from django.urls import path, include
from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
import mimetypes

def serve_index(request):
    index_path = settings.BASE_DIR.parent / 'frontend' / 'index.html'
    try:
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    except Exception:
        return HttpResponseNotFound('Index not found')

def serve_asset(request, asset):
    asset_path = settings.BASE_DIR.parent / 'frontend' / asset
    if asset_path.exists() and asset_path.is_file():
        content_type, _ = mimetypes.guess_type(str(asset_path))
        return FileResponse(open(asset_path, 'rb'), content_type=content_type or 'application/octet-stream')
    return HttpResponseNotFound('Not found')

urlpatterns = [
    path('', serve_index),
    path('<path:asset>', serve_asset),
    path('api/tasks/', include('tasks.urls')),
]
 