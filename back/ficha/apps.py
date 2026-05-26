from django.apps import AppConfig


class FichaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ficha'

    def ready(self):
        import ficha.signals  # noqa: F401