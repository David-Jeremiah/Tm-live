from django.db import migrations, models
import catalogue.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(
                    choices=[
                        ('weddings',    'Weddings'),
                        ('corporate',   'Corporate Events'),
                        ('conferences', 'Conferences & Seminars'),
                        ('intro',       'Introduction Ceremonies'),
                        ('church',      'Church & Worship'),
                        ('outdoor',     'Outdoor Gatherings'),
                    ],
                    db_index=True, max_length=30
                )),
                ('image',     models.ImageField(upload_to=catalogue.models.gallery_upload_path)),
                ('caption',   models.CharField(blank=True, max_length=200)),
                ('order',     models.PositiveIntegerField(default=0, help_text='Lower = first')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['category', 'order', 'id'],
                     'verbose_name': 'Gallery Image',
                     'verbose_name_plural': 'Gallery Images'},
        ),
        migrations.CreateModel(
            name='CorporatePackage',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',        models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('price_min',   models.IntegerField(help_text='Min price in UGX')),
                ('price_max',   models.IntegerField(help_text='Max price in UGX (use same as min for fixed price)')),
                ('includes',    models.TextField(help_text="What's included — one item per line")),
                ('ideal_for',   models.CharField(blank=True, max_length=300)),
                ('order',       models.PositiveIntegerField(default=0)),
                ('is_active',   models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'price_min'],
                     'verbose_name': 'Corporate Package',
                     'verbose_name_plural': 'Corporate Packages'},
        ),
    ]
