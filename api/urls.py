from django.contrib import admin
from django.urls import path, include
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API GameVision",
        default_version='v1',
        description="API para obter informações sobre os dados cadastrados no sistema GameVision",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="game.vision.udf@gmail.com"),
    ),
    public=True,
)


urlpatterns = [
    path('v1/estatisticas/', views.api_player_stats_total, name='api_player_stats_total'),
    path('v1/jogadores/', views.api_players, name='api_players'),
    path('v1/times/', views.api_teams, name='api_teams'),
    path('v1/partidas/', views.api_matches, name='api_matches'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]