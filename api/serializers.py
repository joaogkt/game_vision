from rest_framework import serializers
from player_stats.models import PlayerDesempenhoGeral, PlayerStats
from players.models import Player
from teams.models import Team
from matches.models import Matches

class PlayerDesempenhoGeralSerializer(serializers.ModelSerializer):
    jogador_nome = serializers.CharField(source='jogador.__str__', read_only=True)

    class Meta:
        model = PlayerDesempenhoGeral
        fields = ['jogador_nome', 'total_gols', 'total_assistencias', 'total_passes_certos',
                  'total_passes_errados', 'total_desarmes', 'total_cartoes_vermelhos',
                  'total_cartoes_amarelos', 'media_nota', 'total_partidas']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'city', 'country', 'founded_year', 'logo']

class TeamMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer() 
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'birth_date', 'nationality', 'position', 'photo', 'team']

class MatchesSerializer(serializers.ModelSerializer):

    time_casa = TeamMinimalSerializer()
    time_fora = TeamMinimalSerializer()

    class Meta:
        model = Matches
        fields = ['local', 'time_casa', 'time_fora', 'placar_casa', 'placar_fora', 'data_partida', 'tipo_competicao']

class PlayerStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerStats
        fields = ['jogador', 'jogo', 'minutos_jogados', 'gols', 'assistencia', 'passes_certos', 'passes_errados', 'desarmes', 
                  'cartao_vermelho', 'cartao_amarelo', 'nota']