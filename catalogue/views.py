from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json

from .models import SoundPackage, LightingPackage, Quote


def catalogue(request):
    """Public catalogue page showing all packages."""
    sound_packages = SoundPackage.objects.filter(is_active=True)
    lighting_packages = LightingPackage.objects.filter(is_active=True)
    return render(request, 'catalogue/catalogue.html', {
        'sound_packages': sound_packages,
        'lighting_packages': lighting_packages,
    })


def budget_calculator(request):
    """Budget calculator — enter budget, get matched packages."""
    context = {
        'results': None,
        'budget': None,
        'combinations': [],
    }

    if request.method == 'POST' or request.GET.get('budget'):
        raw = request.POST.get('budget') or request.GET.get('budget', '')
        try:
            budget = int(str(raw).replace(',', '').replace(' ', ''))
        except (ValueError, TypeError):
            budget = None

        if budget:
            context['budget'] = budget

            sound_packages = SoundPackage.objects.filter(is_active=True, price_min__lte=budget)
            lighting_packages = LightingPackage.objects.filter(is_active=True, price_min__lte=budget)

            # Find sound+lighting combinations within budget
            combinations = []
            for sp in SoundPackage.objects.filter(is_active=True):
                for lp in LightingPackage.objects.filter(is_active=True):
                    total = sp.price_min + lp.price_min
                    if total <= budget:
                        combinations.append({
                            'sound': sp,
                            'lighting': lp,
                            'total': total,
                            'remaining': budget - total,
                        })

            # Sort by total descending (best combo first)
            combinations.sort(key=lambda x: x['total'], reverse=True)
            # Keep top 6 combos
            combinations = combinations[:6]

            context['sound_packages'] = sound_packages
            context['lighting_packages'] = lighting_packages
            context['combinations'] = combinations
            context['has_results'] = sound_packages.exists() or lighting_packages.exists()

    return render(request, 'catalogue/budget_calculator.html', context)


def package_detail(request, package_type, pk):
    """Detail view for a single package."""
    if package_type == 'sound':
        package = get_object_or_404(SoundPackage, pk=pk, is_active=True)
        template = 'catalogue/sound_detail.html'
    else:
        package = get_object_or_404(LightingPackage, pk=pk, is_active=True)
        template = 'catalogue/lighting_detail.html'
    return render(request, template, {'package': package, 'package_type': package_type})


def request_quote(request):
    """Quote request form."""
    sound_packages = SoundPackage.objects.filter(is_active=True)
    lighting_packages = LightingPackage.objects.filter(is_active=True)

    if request.method == 'POST':
        # Pre-fill from GET params (e.g., from calculator)
        sound_id = request.POST.get('sound_package')
        lighting_id = request.POST.get('lighting_package')

        quote = Quote(
            client_name=request.POST.get('client_name', ''),
            client_phone=request.POST.get('client_phone', ''),
            client_email=request.POST.get('client_email', ''),
            event_type=request.POST.get('event_type', ''),
            venue=request.POST.get('venue', ''),
            notes=request.POST.get('notes', ''),
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

        # Build WhatsApp message
        msg_parts = [f"*New Quote Request from TM Live Website*"]
        msg_parts.append(f"Name: {quote.client_name}")
        msg_parts.append(f"Phone: {quote.client_phone}")
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

        import urllib.parse
        wa_msg = urllib.parse.quote('\n'.join(msg_parts))
        wa_url = f"https://wa.me/256777523280?text={wa_msg}"

        return render(request, 'catalogue/quote_success.html', {
            'quote': quote,
            'wa_url': wa_url,
        })

    # Pre-select packages from GET params
    pre_sound = request.GET.get('sound')
    pre_lighting = request.GET.get('lighting')

    return render(request, 'catalogue/request_quote.html', {
        'sound_packages': sound_packages,
        'lighting_packages': lighting_packages,
        'pre_sound': pre_sound,
        'pre_lighting': pre_lighting,
    })


def home(request):
    """Landing page."""
    sound_packages = SoundPackage.objects.filter(is_active=True)
    lighting_packages = LightingPackage.objects.filter(is_active=True)
    return render(request, 'catalogue/home.html', {
        'sound_count': sound_packages.count(),
        'lighting_count': lighting_packages.count(),
    })
