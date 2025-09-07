from rest_framework import serializers
from .models import RequestLog, BlockedIP, SuspiciousIP


class RequestLogSerializer(serializers.ModelSerializer):
    """Serializer for RequestLog model."""

    class Meta:
        model = RequestLog
        fields = "__all__"
        extra_kwargs = {
            "ip_address": {"help_text": "Client IP address that made the request"},
            "timestamp": {"help_text": "Date and time when the request was logged"},
            "path": {"help_text": "Path that was accessed by the request"},
            "country": {"help_text": "Country detected from IP address"},
            "city": {"help_text": "City detected from IP address"},
        }


class BlockedIPSerializer(serializers.ModelSerializer):
    """Serializer for BlockedIP model."""

    class Meta:
        model = BlockedIP
        fields = "__all__"
        extra_kwargs = {
            "ip_address": {"help_text": "IP address blocked from accessing the application"},
        }


class SuspiciousIPSerializer(serializers.ModelSerializer):
    """Serializer for SuspiciousIP model."""

    class Meta:
        model = SuspiciousIP
        fields = "__all__"
        extra_kwargs = {
            "ip_address": {"help_text": "Suspicious IP address flagged by security system"},
            "reason": {"help_text": "Reason why this IP was flagged as suspicious"},
            "detected_at": {"help_text": "Timestamp when suspicious activity was detected"},
        }
