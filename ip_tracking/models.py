from django.db import models


class RequestLog(models.Model):
    """Stores details of each incoming request."""
    ip_address = models.GenericIPAddressField(
        help_text="Client IP address"
    )
    timestamp = models.DateTimeField(
        help_text="Date and time when the request was logged"
    )
    path = models.CharField(
        max_length=200,
        help_text="Path requested by the client (e.g., /login)"
    )
    country = models.CharField(   # fixed typo: 'coutry' → 'country'
        max_length=100,
        blank=True,
        null=True,
        help_text="Country resolved from the IP address"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City resolved from the IP address"
    )
    
    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp}"


class BlockedIP(models.Model):
    """Stores IPs that are blocked from accessing the application."""
    ip_address = models.GenericIPAddressField(
        unique=True,
        help_text="IP address blocked from accessing the application"
    )

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

    def __str__(self):
        return f"Blocked IP: {self.ip_address}"


class SuspiciousIP(models.Model):
    """Tracks IP addresses flagged for unusual or malicious behavior."""
    ip_address = models.GenericIPAddressField(
        help_text="Suspicious IP address flagged by anomaly detection"
    )
    reason = models.TextField(
        help_text="Reason this IP was flagged (e.g., >100 requests/hour)"
    )
    detected_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time when suspicious behavior was detected"
    )

    class Meta:
        ordering = ["-detected_at"]
        verbose_name = "Suspicious IP"
        verbose_name_plural = "Suspicious IPs"

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
