from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SoundPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tier', models.IntegerField(choices=[(1,'Essential'),(2,'Standard'),(3,'Wedding Pro'),(4,'Premium'),(5,'Concert'),(6,'Full PA')], unique=True)),
                ('price_min', models.IntegerField(help_text='Minimum price in UGX')),
                ('price_max', models.IntegerField(help_text='Maximum price in UGX')),
                ('tagline', models.CharField(blank=True, max_length=200)),
                ('ideal_for', models.CharField(max_length=300)),
                ('capacity', models.CharField(max_length=100)),
                ('equipment', models.TextField(help_text='One item per line')),
                ('services', models.TextField(help_text='One item per line')),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['tier']},
        ),
        migrations.CreateModel(
            name='LightingPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tier', models.IntegerField(choices=[(1,'Basic'),(2,'Celebration'),(3,'Wedding Signature'),(4,'Wedding Premium'),(5,'Show Pro'),(6,'Full Lighting Production')], unique=True)),
                ('price_min', models.IntegerField(help_text='Minimum price in UGX')),
                ('price_max', models.IntegerField(help_text='Maximum price in UGX')),
                ('tagline', models.CharField(blank=True, max_length=200)),
                ('ideal_for', models.CharField(max_length=300)),
                ('equipment', models.TextField(help_text='One item per line')),
                ('services', models.TextField(help_text='One item per line')),
                ('notes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['tier']},
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=150)),
                ('client_phone', models.CharField(max_length=30)),
                ('client_email', models.EmailField(blank=True)),
                ('event_type', models.CharField(max_length=100)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('venue', models.CharField(blank=True, max_length=200)),
                ('guest_count', models.IntegerField(blank=True, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('draft','Draft'),('sent','Sent'),('accepted','Accepted'),('declined','Declined')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sound_package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.soundpackage')),
                ('lighting_package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.lightingpackage')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
