from django.apps import AppConfig


class ManageUsersConfig(AppConfig):
    name = 'manage_users'
    verbose_name = 'Manage Users'

    def ready(self):
        import manage_users.signals
