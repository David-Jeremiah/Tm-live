from django.db import models


class SoundPackage(models.Model):
    TIER_CHOICES = [
        (1, 'Essential'),
        (2, 'Standard'),
        (3, 'Wedding Pro'),
        (4, 'Premium'),
        (5, 'Concert'),
        (6, 'Full PA'),
    ]

    name = models.CharField(max_length=100)
    tier = models.IntegerField(choices=TIER_CHOICES, unique=True)
    price_min = models.IntegerField(help_text="Minimum price in UGX")
    price_max = models.IntegerField(help_text="Maximum price in UGX")
    tagline = models.CharField(max_length=200, blank=True)
    ideal_for = models.CharField(max_length=300)
    capacity = models.CharField(max_length=100)
    equipment = models.TextField(help_text="One item per line")
    services = models.TextField(help_text="One item per line")
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['tier']

    def __str__(self):
        return f"{self.name} (UGX {self.price_min:,} – {self.price_max:,})"

    def equipment_list(self):
        return [e.strip() for e in self.equipment.strip().splitlines() if e.strip()]

    def services_list(self):
        return [s.strip() for s in self.services.strip().splitlines() if s.strip()]

    def price_display(self):
        if self.price_max >= 1_000_000:
            lo = f"{self.price_min / 1_000_000:.1f}M".rstrip('0').rstrip('.')
            hi = f"{self.price_max / 1_000_000:.1f}M+".rstrip('0').rstrip('.')
            return f"UGX {lo}–{hi}"
        lo = f"{self.price_min // 1000}K"
        hi = f"{self.price_max // 1000}K"
        return f"UGX {lo}–{hi}"


class LightingPackage(models.Model):
    TIER_CHOICES = [
        (1, 'Basic'),
        (2, 'Celebration'),
        (3, 'Wedding Signature'),
        (4, 'Wedding Premium'),
        (5, 'Show Pro'),
        (6, 'Full Lighting Production'),
    ]

    name = models.CharField(max_length=100)
    tier = models.IntegerField(choices=TIER_CHOICES, unique=True)
    price_min = models.IntegerField(help_text="Minimum price in UGX")
    price_max = models.IntegerField(help_text="Maximum price in UGX")
    tagline = models.CharField(max_length=200, blank=True)
    ideal_for = models.CharField(max_length=300)
    equipment = models.TextField(help_text="One item per line")
    services = models.TextField(help_text="One item per line")
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['tier']

    def __str__(self):
        return f"{self.name} (UGX {self.price_min:,} – {self.price_max:,})"

    def equipment_list(self):
        return [e.strip() for e in self.equipment.strip().splitlines() if e.strip()]

    def services_list(self):
        return [s.strip() for s in self.services.strip().splitlines() if s.strip()]

    def price_display(self):
        if self.price_max >= 1_000_000:
            lo = f"{self.price_min / 1_000_000:.1f}M"
            hi = f"{self.price_max / 1_000_000:.1f}M+"
            return f"UGX {lo}–{hi}"
        lo = f"{self.price_min // 1000}K"
        hi = f"{self.price_max // 1000}K"
        return f"UGX {lo}–{hi}"


class Quote(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    client_name = models.CharField(max_length=150)
    client_phone = models.CharField(max_length=30)
    client_email = models.EmailField(blank=True)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    guest_count = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    sound_package = models.ForeignKey(SoundPackage, null=True, blank=True, on_delete=models.SET_NULL)
    lighting_package = models.ForeignKey(LightingPackage, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Quote for {self.client_name} — {self.event_type}"

    def total_price(self):
        total = 0
        if self.sound_package:
            total += self.sound_package.price_min
        if self.lighting_package:
            total += self.lighting_package.price_min
        return total
