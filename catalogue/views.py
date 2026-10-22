from django.shortcuts import render, get_object_or_404
import os

from .models import (
    SiteSettings, ServiceCard,
    SoundPackage, LightingPackage,
    Quote, GalleryImage, CorporatePackage,
)


# ─── helpers ──────────────────────────────────────────────────────────────────

CAT_META = [
    {'key': 'weddings',     'label': '💍 Weddings'},
    {'key': 'corporate',    'label': '🏢 Corporate Events'},
    {'key': 'conferences',  'label': '🎤 Conferences & Seminars'},
    {'key': 'intro',        'label': '🎊 Introduction Ceremonies'},
    {'key': 'church',       'label': '✝ Church & Worship'},
    {'key': 'outdoor',      'label': '🌿 Outdoor Gatherings'},
]


def _build_gallery(settings_obj=None):
    """Return gallery_cats list — DB images first, static fallback."""
    from django.conf import settings as django_settings

    db_images = GalleryImage.objects.filter(is_active=True).order_by('category', 'order', 'id')
    db_by_cat = {}
    for img in db_images:
        db_by_cat.setdefault(img.category, []).append({
            'url': img.image.url,
            'caption': img.caption,
            'from_db': True,
        })

    img_dir = os.path.join(django_settings.BASE_DIR, 'static', 'img')
    gallery_cats = []
    for cat in CAT_META:
        key = cat['key']
        if key in db_by_cat:
            items = db_by_cat[key]
        else:
            try:
                files = sorted([f for f in os.listdir(img_dir) if f.startswith(key + '_')])
            except FileNotFoundError:
                files = []
            items = [{'url': None, 'static_path': f'img/{f}', 'from_db': False} for f in files]

        gallery_cats.append({'key': key, 'label': cat['label'], 'items': items})
    return gallery_cats


# ─── views ────────────────────────────────────────────────────────────────────

def home(request):
    s = SiteSettings.get()
    services = ServiceCard.objects.filter(is_active=True)
    gallery_cats = _build_gallery()

    return render(request, 'catalogue/home.html', {
        's': s,
        'services': services,
        'gallery_cats': gallery_cats,
    })


def catalogue(request):
    sound_packages = SoundPackage.objects.filter(is_active=True)
    lighting_packages = LightingPackage.objects.filter(is_active=True)
    s = SiteSettings.get()
    return render(request, 'catalogue/catalogue.html', {
        's': s,
        'sound_packages': sound_packages,
        'lighting_packages': lighting_packages,
    })


def budget_calculator(request):
    s = SiteSettings.get()
    context = {'results': None, 'budget': None, 'combinations': [], 's': s}

    if request.method == 'POST' or request.GET.get('budget'):
        raw = request.POST.get('budget') or request.GET.get('budget', '')
        try:
            budget = int(str(raw).replace(',', '').replace(' ', ''))
        except (ValueError, TypeError):
            budget = None

        if budget:
            context['budget'] = budget
            sound_packages   = SoundPackage.objects.filter(is_active=True, price_min__lte=budget)
            lighting_packages = LightingPackage.objects.filter(is_active=True, price_min__lte=budget)

            combinations = []
            for sp in SoundPackage.objects.filter(is_active=True):
                for lp in LightingPackage.objects.filter(is_active=True):
                    total = sp.price_min + lp.price_min
                    if total <= budget:
                        combinations.append({
                            'sound': sp, 'lighting': lp,
                            'total': total, 'remaining': budget - total,
                        })

            combinations.sort(key=lambda x: x['total'], reverse=True)
            combinations = combinations[:6]

            context['sound_packages']   = sound_packages
            context['lighting_packages'] = lighting_packages
            context['combinations']     = combinations
            context['has_results']      = sound_packages.exists() or lighting_packages.exists()

    return render(request, 'catalogue/budget_calculator.html', context)


def package_detail(request, package_type, pk):
    s = SiteSettings.get()
    if package_type == 'sound':
        package  = get_object_or_404(SoundPackage,   pk=pk, is_active=True)
        template = 'catalogue/sound_detail.html'
    else:
        package  = get_object_or_404(LightingPackage, pk=pk, is_active=True)
        template = 'catalogue/lighting_detail.html'
    return render(request, template, {'package': package, 'package_type': package_type, 's': s})


def request_quote(request):
    s = SiteSettings.get()
    sound_packages    = SoundPackage.objects.filter(is_active=True)
    lighting_packages = LightingPackage.objects.filter(is_active=True)

    if request.method == 'POST':
        sound_id    = request.POST.get('sound_package')
        lighting_id = request.POST.get('lighting_package')

        quote = Quote(
            client_name  = request.POST.get('client_name', ''),
            client_phone = request.POST.get('client_phone', ''),
            client_email = request.POST.get('client_email', ''),
            event_type   = request.POST.get('event_type', ''),
            venue        = request.POST.get('venue', ''),
            notes        = request.POST.get('notes', ''),
        )
        if request.POST.get('event_date'):
            quote.event_date = request.POST.get('event_date')
        if request.POST.get('guest_count'):
            try:
                quote.guest_count = int(request.POST.get('guest_count'))
            except ValueError:
                pass
        if sound_id:
            try:
                quote.sound_package = SoundPackage.objects.get(pk=sound_id)
            except SoundPackage.DoesNotExist:
                pass
        if lighting_id:
            try:
                quote.lighting_package = LightingPackage.objects.get(pk=lighting_id)
            except LightingPackage.DoesNotExist:
                pass

        quote.save()

        import urllib.parse
        msg_parts = [
            f"*New Quote Request from TM Live Website*",
            f"Name: {quote.client_name}",
            f"Phone: {quote.client_phone}",
        ]
        if quote.client_email:
            msg_parts.append(f"Email: {quote.client_email}")
        msg_parts.append(f"Event: {quote.event_type}")
        if quote.event_date:
            msg_parts.append(f"Date: {quote.event_date}")
        if quote.venue:
            msg_parts.append(f"Venue: {quote.venue}")
        if quote.guest_count:
            msg_parts.append(f"Guests: {quote.guest_count}")
        if quote.sound_package:
            msg_parts.append(f"Sound: {quote.sound_package.name}")
        if quote.lighting_package:
            msg_parts.append(f"Lighting: {quote.lighting_package.name}")
        if quote.notes:
            msg_parts.append(f"Notes: {quote.notes}")

        wa_msg = urllib.parse.quote('\n'.join(msg_parts))
        wa_url = f"https://wa.me/{s.wa1_digits()}?text={wa_msg}"

        return render(request, 'catalogue/quote_success.html', {
            'quote': quote, 'wa_url': wa_url, 's': s,
        })

    pre_sound    = request.GET.get('sound')
    pre_lighting = request.GET.get('lighting')

    return render(request, 'catalogue/request_quote.html', {
        's': s,
        'sound_packages':    sound_packages,
        'lighting_packages': lighting_packages,
        'pre_sound':    pre_sound,
        'pre_lighting': pre_lighting,
    })


def corporate(request):
    s = SiteSettings.get()
    packages = CorporatePackage.objects.filter(is_active=True)
    return render(request, 'catalogue/corporate.html', {'packages': packages, 's': s})
