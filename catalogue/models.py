from django.db import models
import os


# ─── Upload helpers ────────────────────────────────────────────────────────────

def gallery_upload_path(instance, filename):
    return f"gallery/{instance.category}/{filename}"

def hero_upload_path(instance, filename):
    return f"site/hero/{filename}"

def logo_upload_path(instance, filename):
    return f"site/logo/{filename}"


# ─── Site Settings (singleton) ─────────────────────────────────────────────────

class SiteSettings(models.Model):
    """Single-row table that drives the whole homepage.
    Admin edits here are immediately reflected on the live site."""

    # Branding
    site_name     = models.CharField(max_length=100, default="TM Live")
    tagline       = models.CharField(max_length=200, default="Your Event. Our Sound. Perfection Guaranteed.")
    logo          = models.ImageField(upload_to=logo_upload_path, blank=True, null=True,
                                      help_text="Logo shown in the hero circle")

    # Hero
    hero_image    = models.ImageField(upload_to=hero_upload_path, blank=True, null=True,
                                      help_text="Background image for the hero section (optional)")
    hero_line1    = models.CharField(max_length=60, default="YOUR EVENT",
                                     help_text="First cycling headline line")
    hero_line2    = models.CharField(max_length=60, default="OUR SOUND",
                                     help_text="Second cycling headline line")
    hero_line3    = models.CharField(max_length=60, default="PERFECTION",
                                     help_text="Third cycling headline line")
    hero_line4    = models.CharField(max_length=60, default="GUARANTEED",
                                     help_text="Fourth cycling headline line")
    hero_verse    = models.CharField(max_length=300,
                                     default="Professional Sound. Honouring Your Faith. Glorifying Christ.",
                                     help_text="Small italic text above the headline")

    # Contact details
    phone_calls   = models.CharField(max_length=30, default="+256704995334",
                                     help_text="Primary phone (calls)")
    phone_wa1     = models.CharField(max_length=30, default="+256777523280",
                                     help_text="WhatsApp number 1")
    phone_wa2     = models.CharField(max_length=30, default="+256750329798",
                                     help_text="WhatsApp number 2 (leave blank to hide)")
    email         = models.EmailField(default="tmlive256@gmail.com")
    location      = models.CharField(max_length=100, default="Uganda")

    # Vision / About
    vision_title  = models.CharField(max_length=200,
                                     default="Professional Sound. Honouring Your Faith. Glorifying Christ.")
    vision_body   = models.TextField(
        default=(
            "TM Live is a Trusted PA System and Live Sound Provider Company committed to delivering "
            "exceptional audio experiences with Professionalism, Integrity, and Excellence. Whether "
            "you're hosting a celebration, a corporate gathering, a church event, or a community "
            "function, we provide reliable sound solutions tailored to your event's needs.\n\n"
            "Our foundation is rooted in Christian values, guiding us to serve every client with "
            "honesty, respect, and a commitment to excellence. Honouring both your Faith and Christ.\n\n"
            "We believe every event deserves sound that is clear, engaging, and memorable. 🎶"
        ),
        help_text="Supports line breaks. Use **bold** for emphasis."
    )

    # Footer
    footer_note   = models.CharField(max_length=300,
                                     default="© 2025 TM Live · Live Sound & PA · Uganda",
                                     blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def get(cls):
        """Always returns the one settings row, creating it if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def wa1_digits(self):
        """Phone digits only for wa.me links"""
        return ''.join(c for c in self.phone_wa1 if c.isdigit())

    def wa2_digits(self):
        return ''.join(c for c in self.phone_wa2 if c.isdigit())

    def calls_digits(self):
        return ''.join(c for c in self.phone_calls if c.isdigit())


# ─── Service Cards ─────────────────────────────────────────────────────────────

class ServiceCard(models.Model):
    """Each card in the 'What We Offer' grid on the homepage."""
    icon        = models.CharField(max_length=10, default="🎤",
                                   help_text="Emoji icon shown on the card")
    name        = models.CharField(max_length=80)
    highlight   = models.CharField(max_length=150, blank=True,
                                   help_text="Short gold text shown at the top of the description")
    description = models.CharField(max_length=300)
    order       = models.PositiveIntegerField(default=0, help_text="Lower = shown first")
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Service Card"
        verbose_name_plural = "Service Cards"

    def __str__(self):
        return f"{self.icon} {self.name}"


# ─── Sound Package ─────────────────────────────────────────────────────────────

class SoundPackage(models.Model):
    TIER_CHOICES = [
        (1, 'Essential'),
        (2, 'Standard'),
        (3, 'Wedding Pro'),
        (4, 'Premium'),
        (5, 'Concert'),
        (6, 'Full PA'),
    ]

    name      = models.CharField(max_length=100)
    tier      = models.IntegerField(choices=TIER_CHOICES, unique=True)
    price_min = models.IntegerField(help_text="Minimum price in UGX")
    price_max = models.IntegerField(help_text="Maximum price in UGX")
    tagline   = models.CharField(max_length=200, blank=True)
    ideal_for = models.CharField(max_length=300)
    capacity  = models.CharField(max_length=100)
    equipment = models.TextField(help_text="One item per line")
    services  = models.TextField(help_text="One item per line")
    notes     = models.TextField(blank=True)
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
        lo = f"UGX {self.price_min:,}"
        hi = f"{self.price_max:,}"
        return f"{lo} – {hi}"


# ─── Lighting Package ──────────────────────────────────────────────────────────

class LightingPackage(models.Model):
    TIER_CHOICES = [
        (1, 'Basic'),
        (2, 'Celebration'),
        (3, 'Wedding Signature'),
        (4, 'Wedding Premium'),
        (5, 'Show Pro'),
        (6, 'Full Lighting Production'),
    ]

    name      = models.CharField(max_length=100)
    tier      = models.IntegerField(choices=TIER_CHOICES, unique=True)
    price_min = models.IntegerField(help_text="Minimum price in UGX")
    price_max = models.IntegerField(help_text="Maximum price in UGX")
    tagline   = models.CharField(max_length=200, blank=True)
    ideal_for = models.CharField(max_length=300)
    equipment = models.TextField(help_text="One item per line")
    services  = models.TextField(help_text="One item per line")
    notes     = models.TextField(blank=True)
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
        lo = f"UGX {self.price_min:,}"
        hi = f"{self.price_max:,}"
        return f"{lo} – {hi}"


# ─── Quote ─────────────────────────────────────────────────────────────────────

class Quote(models.Model):
    STATUS_CHOICES = [
        ('draft',    'Draft'),
        ('sent',     'Sent'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    client_name      = models.CharField(max_length=150)
    client_phone     = models.CharField(max_length=30)
    client_email     = models.EmailField(blank=True)
    event_type       = models.CharField(max_length=100)
    event_date       = models.DateField(null=True, blank=True)
    venue            = models.CharField(max_length=200, blank=True)
    guest_count      = models.IntegerField(null=True, blank=True)
    budget           = models.IntegerField(null=True, blank=True)
    sound_package    = models.ForeignKey(SoundPackage,   null=True, blank=True, on_delete=models.SET_NULL)
    lighting_package = models.ForeignKey(LightingPackage, null=True, blank=True, on_delete=models.SET_NULL)
    notes            = models.TextField(blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

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


# ─── Gallery Image ─────────────────────────────────────────────────────────────

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('weddings',    'Weddings'),
        ('corporate',   'Corporate Events'),
        ('conferences', 'Conferences & Seminars'),
        ('intro',       'Introduction Ceremonies'),
        ('church',      'Church & Worship'),
        ('outdoor',     'Outdoor Gatherings'),
    ]

    category  = models.CharField(max_length=30, choices=CATEGORY_CHOICES, db_index=True)
    image     = models.ImageField(upload_to=gallery_upload_path)
    caption   = models.CharField(max_length=200, blank=True)
    order     = models.PositiveIntegerField(default=0, help_text="Lower = first")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'id']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"{self.get_category_display()} — {os.path.basename(self.image.name)}"


# ─── Corporate Package ─────────────────────────────────────────────────────────

class CorporatePackage(models.Model):
    name        = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price_min   = models.IntegerField(help_text="Min price in UGX")
    price_max   = models.IntegerField(help_text="Max price in UGX (same as min = fixed price)")
    includes    = models.TextField(help_text="What's included — one item per line")
    ideal_for   = models.CharField(max_length=300, blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'price_min']
        verbose_name = 'Corporate Package'
        verbose_name_plural = 'Corporate Packages'

    def __str__(self):
        return f"{self.name} — UGX {self.price_min:,}"

    def includes_list(self):
        return [i.strip() for i in self.includes.strip().splitlines() if i.strip()]

    def price_display(self):
        lo = f"UGX {self.price_min:,}"
        if self.price_max and self.price_max != self.price_min:
            return f"{lo} – {self.price_max:,}"
        return lo
