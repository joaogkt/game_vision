from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PlayerDesempenhoGeralSerializer, PlayerSerializer
from player_stats.models import PlayerDesempenhoGeral
from players.models import Player
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


@swagger_auto_schema(
    method='get',
    operation_description="Obtém todas as estatísticas de desempenho dos jogadores.",
    responses={200: PlayerDesempenhoGeralSerializer(many=True)},
)
@api_view(['GET'])
def api_player_stats_total(request):
    desempenhos = PlayerDesempenhoGeral.objects.all()
    serializer = PlayerDesempenhoGeralSerializer(desempenhos, many=True)
    return Response(serializer.data)



@swagger_auto_schema(
    method='get',
    operation_description="Obtém todos os jogadores cadastrados.",
    responses={200: PlayerSerializer(many=True)},
)
@api_view(["GET"])
def api_players(request):
    jogadores = Player.objects.all()
    serializer = PlayerSerializer(jogadores, many=True)
    return Response(serializer.data)