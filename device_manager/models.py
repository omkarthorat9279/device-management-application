from django.db import models
from django.utils import timezone

class Device(models.Model):
    ip_address = models.CharField(max_length=15, unique=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=255, blank=True, null=True)
    ping_status = models.BooleanField(default=False)
    ping_output = models.TextField(blank=True, null=True)
    dc_network = models.CharField(max_length=255, blank=True, null=True)
    asn_network = models.CharField(max_length=255, blank=True, null=True)
    asn_route = models.CharField(max_length=255, blank=True, null=True)
    location_latitude = models.FloatField(blank=True, null=True)
    location_longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ip_address} - {self.hostname or 'No Hostname'}"

    class Meta:
        ordering = ['-created_at']
