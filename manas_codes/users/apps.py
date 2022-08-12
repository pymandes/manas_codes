from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "manas_codes.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import manas_codes.users.signals  # noqa F401
        except ImportError:
            pass
