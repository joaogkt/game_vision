from rest_framework import serializers
from player_stats.models import PlayerDesempenhoGeral
from players.models import Player

class PlayerDesempenhoGeralSerializer(serializers.ModelSerializer):
    jogador_nome = serializers.CharField(source='jogador.__str__', read_only=True)

    class Meta:
        model = PlayerDesempenhoGeral
        fields = ['jogador_nome', 'total_gols', 'total_assistencias', 'total_passes_certos',
                  'total_passes_errados', 'total_desarmes', 'total_cartoes_vermelhos',
                  'total_cartoes_amarelos', 'media_nota', 'total_partidas']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'birth_date', 'nationality', 'position', 'team', 'photo']
