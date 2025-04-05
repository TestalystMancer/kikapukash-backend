from django.apps import AppConfig


class SavingsGroupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'savings_group'

    def ready(self):
        import savings_group.signals