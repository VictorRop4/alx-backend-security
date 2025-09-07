from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import RequestLog, BlockedIP, SuspiciousIP
from .serializers import RequestLogSerializer, BlockedIPSerializer, SuspiciousIPSerializer


# -------------------------
# API ViewSets (Token Authentication)
# -------------------------

class RequestLogViewSet(viewsets.ModelViewSet):
    queryset = RequestLog.objects.all().order_by("-timestamp")
    serializer_class = RequestLogSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all request logs.",
        security=[{'Token': []}],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new Request Log",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ip_address": openapi.Schema(type=openapi.TYPE_STRING, example="192.168.1.1"),
                "path": openapi.Schema(type=openapi.TYPE_STRING, example="/api/login/"),
                "method": openapi.Schema(type=openapi.TYPE_STRING, example="POST"),
                "country": openapi.Schema(type=openapi.TYPE_STRING, example="Kenya"),
                "city": openapi.Schema(type=openapi.TYPE_STRING, example="Nairobi"),
                "timestamp": openapi.Schema(type=openapi.FORMAT_DATETIME, example="2025-09-07T14:30:00Z"),
            }
        ),
        security=[{'Token': []}],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BlockedIPViewSet(viewsets.ModelViewSet):
    queryset = BlockedIP.objects.all()
    serializer_class = BlockedIPSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all blocked IPs.",
        security=[{'Token': []}],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Block a new IP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ip_address": openapi.Schema(type=openapi.TYPE_STRING, example="203.0.113.45"),
            }
        ),
        security=[{'Token': []}],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SuspiciousIPViewSet(viewsets.ModelViewSet):
    queryset = SuspiciousIP.objects.all().order_by("-detected_at")
    serializer_class = SuspiciousIPSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all suspicious IP records.",
        security=[{'Token': []}],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Report a suspicious IP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "ip_address": openapi.Schema(type=openapi.TYPE_STRING, example="198.51.100.25"),
                "reason": openapi.Schema(type=openapi.TYPE_STRING, example="Exceeded 100 requests/hour"),
                "detected_at": openapi.Schema(type=openapi.FORMAT_DATETIME, example="2025-09-07T14:30:00Z"),
            }
        ),
        security=[{'Token': []}],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# -------------------------
# Login View (open access for simulation)
# -------------------------

@swagger_auto_schema(
    method="post",
    operation_summary="Simulated Login",
    operation_description=(
        "Simulates a login request with rate limiting.\n"
        "- Max 5 POST requests/min per IP\n"
        "- Max 10 POST requests/min per user"
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, example="user1"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, example="secret"),
        }
    ),
    responses={
        200: openapi.Response("Successful login response", examples={
            "application/json": {"message": "Authenticated login successful"}
        }),
        429: "Too Many Requests - Rate limit exceeded",
    }
)
@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@ratelimit(key="user", rate="10/m", method="POST", block=True)
def login_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"message": "Authenticated login successful"})
    else:
        return JsonResponse({"message": "Anonymous login successful"})
