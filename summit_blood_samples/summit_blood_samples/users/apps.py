from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "summit_blood_samples.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import summit_blood_samples.users.signals  # noqa F401
        except ImportError:
            pass
