from django.db import models


class RequestLog(models.Model):
    """Stores details of each incoming request."""
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=200)
    coutry = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp}"


class BlockedIP(models.Model):
    """Stores IPs that are blocked from accessing the application."""
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return f"Blocked IP: {self.ip_address}"

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"