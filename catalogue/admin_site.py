"""Custom AdminSite that powers the TM Live dashboard."""

from django.contrib.admin import AdminSite
from django.utils import timezone
from django.db.models import Sum, Count, Q


class TMLiveAdminSite(AdminSite):
    site_header  = "TM Live Admin"
    site_title   = "TM Live"
    index_title  = "Dashboard"

    def index(self, request, extra_context=None):
        from .models import Quote, GalleryImage, SoundPackage, LightingPackage

        now   = timezone.now()
        today = now.date()
        week_start  = today - timezone.timedelta(days=7)
        month_start = today.replace(day=1)

        qs = Quote.objects.all()

        total_quotes    = qs.count()
        accepted_quotes = qs.filter(status='accepted').count()
        declined_quotes = qs.filter(status='declined').count()
        pending_quotes  = qs.filter(status__in=['draft', 'sent']).count()

        today_quotes  = qs.filter(created_at__date=today).count()
        week_quotes   = qs.filter(created_at__date__gte=week_start).count()
        month_quotes  = qs.filter(created_at__date__gte=month_start).count()

        # Revenue approximations (sum of price_min for selected packages)
        def _total_for(queryset):
            total = 0
            for q in queryset.select_related('sound_package', 'lighting_package'):
                if q.sound_package:
                    total += q.sound_package.price_min
                if q.lighting_package:
                    total += q.lighting_package.price_min
            return total

        accepted_total = _total_for(qs.filter(status='accepted'))
        pending_total  = _total_for(qs.filter(status__in=['draft', 'sent']))
        month_total    = _total_for(qs.filter(created_at__date__gte=month_start))

        recent_quotes  = qs.select_related('sound_package', 'lighting_package').order_by('-created_at')[:15]

        gallery_count  = GalleryImage.objects.filter(is_active=True).count()
        sound_count    = SoundPackage.objects.filter(is_active=True).count()
        lighting_count = LightingPackage.objects.filter(is_active=True).count()

        ctx = {
            'total_quotes':    total_quotes,
            'accepted_quotes': accepted_quotes,
            'declined_quotes': declined_quotes,
            'pending_quotes':  pending_quotes,
            'today_quotes':    today_quotes,
            'week_quotes':     week_quotes,
            'month_quotes':    month_quotes,
            'accepted_total':  accepted_total,
            'pending_total':   pending_total,
            'month_total':     month_total,
            'recent_quotes':   recent_quotes,
            'gallery_count':   gallery_count,
            'sound_count':     sound_count,
            'lighting_count':  lighting_count,
        }
        if extra_context:
            ctx.update(extra_context)
        return super().index(request, extra_context=ctx)


# Singleton instance — imported and used in urls.py and admin.py
tm_admin_site = TMLiveAdminSite(name='admin')

# Register Django's built-in auth/session models
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
tm_admin_site.register(User, UserAdmin)
tm_admin_site.register(Group, GroupAdmin)
