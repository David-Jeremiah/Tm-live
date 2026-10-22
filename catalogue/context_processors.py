from .models import SiteSettings


def site_settings(request):
    """Makes `s` (SiteSettings) available in every template automatically."""
    return {'s': SiteSettings.get()}
