from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RequestLogViewSet, BlockedIPViewSet, SuspiciousIPViewSet, login_view

# DRF router for models
router = DefaultRouter()
router.register(r"requestlogs", RequestLogViewSet, basename="requestlog")
router.register(r"blockedips", BlockedIPViewSet, basename="blockedip")
router.register(r"suspiciousips", SuspiciousIPViewSet, basename="suspiciousip")

urlpatterns = [
    # JWT auth endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_create"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh_create"),

    # Model ViewSets
    path("", include(router.urls)),

    # Rate-limited login simulation
    path("login/", login_view, name="login"),
]
