from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json


class XMLget(APIView):
    def get(self, request):
        response = requests.get("http://127.0.0.1:5678/api")
        return JsonResponse(response.json(), json_dumps_params={'ensure_ascii': False})

# def index(request):
#     if request.method == "POST":
#         response = requests.get("http://127.0.0.1:1234/api")
#         return JsonResponse(response.json())
#     else:
#         return render(request, "main/index.html", {})