from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'
    verbose_name = 'Núcleo de sistema'

    def ready(self):
        import apps.core.signals