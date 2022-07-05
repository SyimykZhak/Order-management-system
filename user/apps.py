from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = 'клиенты'

    def ready(self):
        from user import signals