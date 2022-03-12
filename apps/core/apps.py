from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = 'Núcleo de sistema'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import apps.core.signals