from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=15, unique=True)),
                ('hostname', models.CharField(blank=True, max_length=255, null=True)),
                ('serial', models.CharField(blank=True, max_length=255, null=True)),
                ('ping_status', models.BooleanField(default=False)),
                ('ping_output', models.TextField(blank=True, null=True)),
                ('dc_network', models.CharField(blank=True, max_length=255, null=True)),
                ('asn_network', models.CharField(blank=True, max_length=255, null=True)),
                ('asn_route', models.CharField(blank=True, max_length=255, null=True)),
                ('location_latitude', models.FloatField(blank=True, null=True)),
                ('location_longitude', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
