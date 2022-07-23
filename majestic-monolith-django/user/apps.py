from django.apps import AppConfig
from django.contrib import admin


class UserConfig(AppConfig):
    name = "user"

    def ready(self):
        admin.site.disable_action("delete_selected")
