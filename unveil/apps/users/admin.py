"""Admin configuration for users app."""

from django.apps import apps
from django.contrib import admin


# Autoregister any models not already registered
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


for model in apps.get_app_config("users").get_models():
    admin_class = type("AdminClass", (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
