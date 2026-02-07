from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'

    def ready(self):
        # Import signals here to avoid circular dependencies
        import apps.core.signals
