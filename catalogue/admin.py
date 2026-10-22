from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    SiteSettings, ServiceCard,
    SoundPackage, LightingPackage,
    Quote, GalleryImage, CorporatePackage,
)


# ─── Site Settings ─────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton admin — only one row ever exists."""

    fieldsets = (
        ('🎨 Branding', {
            'fields': ('site_name', 'tagline', 'logo'),
            'description': 'Logo and site name shown across the site.',
        }),
        ('🖼️ Hero Section', {
            'fields': ('hero_image', 'hero_verse', 'hero_line1', 'hero_line2', 'hero_line3', 'hero_line4'),
            'description': 'Hero background image and the four cycling headline words.',
        }),
        ('📞 Contact Details', {
            'fields': ('phone_calls', 'phone_wa1', 'phone_wa2', 'email', 'location'),
            'description': 'Shown in the contact strip and footer.',
        }),
        ('📖 Vision / About Section', {
            'fields': ('vision_title', 'vision_body'),
            'description': 'The "Our Vision" section on the homepage.',
        }),
        ('🔻 Footer', {
            'fields': ('footer_note',),
        }),
    )

    readonly_fields = ('logo_preview', 'hero_preview')

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="height:80px;width:80px;object-fit:cover;border-radius:50%;'
                'border:2px solid #F5C518;">',
                obj.logo.url
            )
        return mark_safe('<span style="color:#888">No logo uploaded</span>')
    logo_preview.short_description = 'Logo Preview'

    def hero_preview(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:120px;max-width:300px;object-fit:cover;border-radius:8px;">',
                obj.hero_image.url
            )
        return mark_safe('<span style="color:#888">No hero image uploaded</span>')
    hero_preview.short_description = 'Hero Image Preview'

    def has_add_permission(self, request):
        # Prevent adding a second row
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Skip the list, go straight to edit the single row
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        from django.shortcuts import redirect
        return redirect(f'../1/change/')


# ─── Service Cards ─────────────────────────────────────────────────────────────

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display  = ['icon', 'name', 'highlight', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['name']
    ordering      = ['order']


# ─── Sound Packages ────────────────────────────────────────────────────────────

@admin.register(SoundPackage)
class SoundPackageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'tier', 'price_display', 'ideal_for', 'is_active']
    list_filter   = ['is_active', 'tier']
    list_editable = ['is_active']
    search_fields = ['name', 'ideal_for']
    ordering      = ['tier']
    fieldsets = (
        ('Package Info', {
            'fields': ('name', 'tier', 'tagline', 'ideal_for', 'capacity', 'is_active')
        }),
        ('Pricing (UGX)', {
            'fields': ('price_min', 'price_max'),
            'description': 'Enter amounts in full, e.g. 1500000 for UGX 1,500,000'
        }),
        ('Equipment & Services', {
            'fields': ('equipment', 'services', 'notes'),
            'description': 'Enter one item per line.'
        }),
    )


# ─── Lighting Packages ─────────────────────────────────────────────────────────

@admin.register(LightingPackage)
class LightingPackageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'tier', 'price_display', 'ideal_for', 'is_active']
    list_filter   = ['is_active', 'tier']
    list_editable = ['is_active']
    search_fields = ['name', 'ideal_for']
    ordering      = ['tier']
    fieldsets = (
        ('Package Info', {
            'fields': ('name', 'tier', 'tagline', 'ideal_for', 'is_active')
        }),
        ('Pricing (UGX)', {
            'fields': ('price_min', 'price_max'),
            'description': 'Enter amounts in full, e.g. 1000000 for UGX 1,000,000'
        }),
        ('Equipment & Services', {
            'fields': ('equipment', 'services', 'notes'),
            'description': 'Enter one item per line.'
        }),
    )


# ─── Corporate Packages ────────────────────────────────────────────────────────

@admin.register(CorporatePackage)
class CorporatePackageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'price_display', 'ideal_for', 'order', 'is_active']
    list_filter   = ['is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['name']
    search_fields = ['name', 'ideal_for']
    ordering      = ['order', 'price_min']
    fieldsets = (
        ('Package Info', {
            'fields': ('name', 'description', 'ideal_for', 'order', 'is_active')
        }),
        ('Pricing (UGX)', {
            'fields': ('price_min', 'price_max'),
            'description': 'Set price_max = price_min for a fixed price.'
        }),
        ("What's Included", {
            'fields': ('includes',),
            'description': 'One item per line. Each becomes a ✓ bullet on the card.'
        }),
    )


# ─── Gallery Images ────────────────────────────────────────────────────────────

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ['thumb', 'category', 'caption', 'order', 'is_active']
    list_filter   = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['thumb']
    search_fields = ['caption']
    ordering      = ['category', 'order']

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:52px;width:80px;object-fit:cover;border-radius:5px;">',
                obj.image.url
            )
        return '—'
    thumb.short_description = '📷'


# ─── Quotes ────────────────────────────────────────────────────────────────────

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display    = ['client_name', 'client_phone', 'event_type', 'event_date',
                       'sound_package', 'lighting_package', 'total_display', 'status', 'created_at']
    list_filter     = ['status', 'event_type']
    list_editable   = ['status']
    list_display_links = ['client_name']
    search_fields   = ['client_name', 'client_phone', 'client_email']
    readonly_fields = ['created_at', 'updated_at', 'total_display', 'wa_link']
    ordering        = ['-created_at']

    fieldsets = (
        ('Client', {
            'fields': ('client_name', 'client_phone', 'client_email')
        }),
        ('Event', {
            'fields': ('event_type', 'event_date', 'venue', 'guest_count', 'notes')
        }),
        ('Packages', {
            'fields': ('sound_package', 'lighting_package', 'budget', 'total_display')
        }),
        ('Status', {
            'fields': ('status', 'wa_link', 'created_at', 'updated_at')
        }),
    )

    def total_display(self, obj):
        total = obj.total_price()
        return format_html('<strong style="color:#F5C518">UGX {:,}</strong>', total) if total else '—'
    total_display.short_description = 'Total'

    def wa_link(self, obj):
        import urllib.parse
        parts = [f"*Quote #{obj.pk} — {obj.client_name}*",
                 f"Event: {obj.event_type}"]
        if obj.event_date:
            parts.append(f"Date: {obj.event_date}")
        if obj.sound_package:
            parts.append(f"Sound: {obj.sound_package.name}")
        if obj.lighting_package:
            parts.append(f"Lighting: {obj.lighting_package.name}")
        total = obj.total_price()
        if total:
            parts.append(f"Total: UGX {total:,}")
        msg = urllib.parse.quote('\n'.join(parts))
        s = SiteSettings.get()
        url = f"https://wa.me/{s.wa1_digits()}?text={msg}"
        return format_html('<a href="{}" target="_blank" style="color:#25D366">💬 Send on WhatsApp</a>', url)
    wa_link.short_description = 'WhatsApp'
