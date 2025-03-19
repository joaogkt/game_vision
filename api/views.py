from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PlayerDesempenhoGeralSerializer
from player_stats.models import PlayerDesempenhoGeral

# Create your views here.
@api_view(['GET'])
def api_estatisticas_jogadores(request):
    desempenhos = PlayerDesempenhoGeral.objects.all()
    serializer = PlayerDesempenhoGeralSerializer(desempenhos, many=True)
    return Response(serializer.data)
