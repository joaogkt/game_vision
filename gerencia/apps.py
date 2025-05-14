from django.apps import AppConfig


class GerenciaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gerencia'


class PlayersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'players'

    def ready(self):
        import gerencia.signals
