from django.db import migrations, models
import catalogue.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_galleryimage_corporatepackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name',    models.CharField(default='TM Live', max_length=100)),
                ('tagline',      models.CharField(default='Your Event. Our Sound. Perfection Guaranteed.', max_length=200)),
                ('logo',         models.ImageField(blank=True, null=True, upload_to=catalogue.models.logo_upload_path,
                                                   help_text='Logo shown in the hero circle')),
                ('hero_image',   models.ImageField(blank=True, null=True, upload_to=catalogue.models.hero_upload_path,
                                                   help_text='Background image for the hero section (optional)')),
                ('hero_line1',   models.CharField(default='YOUR EVENT', max_length=60)),
                ('hero_line2',   models.CharField(default='OUR SOUND',  max_length=60)),
                ('hero_line3',   models.CharField(default='PERFECTION', max_length=60)),
                ('hero_line4',   models.CharField(default='GUARANTEED', max_length=60)),
                ('hero_verse',   models.CharField(default='Professional Sound. Honouring Your Faith. Glorifying Christ.',
                                                  max_length=300)),
                ('phone_calls',  models.CharField(default='+256704995334', max_length=30)),
                ('phone_wa1',    models.CharField(default='+256777523280', max_length=30)),
                ('phone_wa2',    models.CharField(default='+256750329798', max_length=30)),
                ('email',        models.EmailField(default='tmlive256@gmail.com')),
                ('location',     models.CharField(default='Uganda', max_length=100)),
                ('vision_title', models.CharField(default='Professional Sound. Honouring Your Faith. Glorifying Christ.',
                                                  max_length=200)),
                ('vision_body',  models.TextField(default='Enter your vision/about text here.')),
                ('footer_note',  models.CharField(blank=True, default='© 2025 TM Live · Live Sound & PA · Uganda',
                                                  max_length=300)),
            ],
            options={'verbose_name': 'Site Settings', 'verbose_name_plural': 'Site Settings'},
        ),
        migrations.CreateModel(
            name='ServiceCard',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon',        models.CharField(default='🎤', max_length=10)),
                ('name',        models.CharField(max_length=80)),
                ('highlight',   models.CharField(blank=True, max_length=150)),
                ('description', models.CharField(max_length=300)),
                ('order',       models.PositiveIntegerField(default=0)),
                ('is_active',   models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'id'],
                     'verbose_name': 'Service Card',
                     'verbose_name_plural': 'Service Cards'},
        ),
    ]
