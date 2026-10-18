from django.contrib import admin
from .models import SoundPackage, LightingPackage, Quote


@admin.register(SoundPackage)
class SoundPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'price_display', 'ideal_for', 'is_active']
    list_filter = ['is_active', 'tier']
    list_editable = ['is_active']
    ordering = ['tier']

    def price_display(self, obj):
        return f"UGX {obj.price_min:,} – {obj.price_max:,}"
    price_display.short_description = 'Price Range'


@admin.register(LightingPackage)
class LightingPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'price_display', 'ideal_for', 'is_active']
    list_filter = ['is_active', 'tier']
    list_editable = ['is_active']
    ordering = ['tier']

    def price_display(self, obj):
        return f"UGX {obj.price_min:,} – {obj.price_max:,}"
    price_display.short_description = 'Price Range'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'event_type', 'event_date', 'sound_package', 'lighting_package', 'status', 'created_at']
    list_filter = ['status', 'event_type']
    search_fields = ['client_name', 'client_phone', 'client_email']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
