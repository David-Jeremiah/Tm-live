from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    name = "catalogue"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        # Import all admin registrations against tm_admin_site
        import catalogue.admin  # noqa: F401
