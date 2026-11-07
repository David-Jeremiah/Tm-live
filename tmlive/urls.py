from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalogue.admin_site import tm_admin_site

urlpatterns = [
    path("admin/", tm_admin_site.urls),
    path("", include("catalogue.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
