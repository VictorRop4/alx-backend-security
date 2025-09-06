from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
@ratelimit(key="user", rate="10/m", method="POST", block=True)
def login_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse({"message": "Authenticated login successful"})
        else:
            return JsonResponse({"message": "Anonymous login successful"})
    return JsonResponse({"message": "Send a POST request to login"})
