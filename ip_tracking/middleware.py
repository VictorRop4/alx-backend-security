from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog, BlockedIP
from django.utils.timezone import now
import requests
from django.core.cache import cache


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get client IP (basic way)
        ip_address = request.META.get('REMOTE_ADDR')

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP is blocked.")
        
        # ✅ Try cache first
        geo_data = cache.get(ip_address)
        if not geo_data:
            try:
                # Use free API (e.g., ipapi.co)
                response = requests.get(f"https://ipapi.co/{ip_address}/json/")
                if response.status_code == 200:
                    data = response.json()
                    geo_data = {
                        "country": data.get("country_name", ""),
                        "city": data.get("city", ""),
                    }
                    # Cache for 24 hours
                    cache.set(ip_address, geo_data, timeout=86400)
                else:
                    geo_data = {"country": "", "city": ""}
            except Exception:
                geo_data = {"country": "", "city": ""}

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path,
            country=geo_data["country"],
            city=geo_data['city']
        )
        return None
