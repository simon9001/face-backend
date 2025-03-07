from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from recognition.views import get_csrf_token, user_login

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf-token'),
    path('admin/', admin.site.urls),
    path('api/', include('recognition.urls')),
    path("api/", include("cameras.urls")),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
