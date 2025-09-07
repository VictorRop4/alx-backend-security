from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions, routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ip_tracking.views import (
    RequestLogViewSet,
    BlockedIPViewSet,
    SuspiciousIPViewSet,
    login_view,
)

# -------------------------
# Swagger Schema with Token Security
# -------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Security API",
        default_version="v1",
        description="API documentation for Security Features",
        terms_of_service="https://opensource.org/licenses/MIT",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Add global token security
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter token as: Token <your_token>'
        }
    }
}

# -------------------------
# DRF Routers
# -------------------------
router = routers.DefaultRouter()
router.register(r"request-logs", RequestLogViewSet, basename="requestlog")
router.register(r"blocked-ips", BlockedIPViewSet, basename="blockedip")
router.register(r"suspicious-ips", SuspiciousIPViewSet, basename="suspiciousip")

# -------------------------
# URL Patterns
# -------------------------
urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    path("api/", include(router.urls)),
    path("api/login/", login_view, name="login"),

    # Token Authentication endpoint
    path("api/token-auth/", obtain_auth_token, name="api_token_auth"),

    # Swagger UI
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
