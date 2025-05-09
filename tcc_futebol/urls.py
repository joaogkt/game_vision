
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/', include('players.urls')),
    path('teams/', include('teams.urls')),
    path('matches/', include('matches.urls')),
    path('stats/', include('player_stats.urls')),
    path('', include('core.urls')),
    path('api/', include('api.urls')),
    path('gerencia/', include('gerencia.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
