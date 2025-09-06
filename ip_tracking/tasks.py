from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Flag IPs with more than 100 requests in the last hour
    or accessing sensitive paths like /admin or /login.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Aggregate requests by IP in the last hour
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        # Flag sensitive paths
        if any(path in log.path for path in ["/admin", "/login"]):
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}"
            )

    # Flag IPs exceeding 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"Exceeded 100 requests/hour: {count}"
            )
