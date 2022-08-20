from django.shortcuts import render
# from django.urls import reverse
from django.http import JsonResponse
import requests
import json

# Create your views here.
def index(request):
    if request.method == "POST":
        response = requests.get("http://127.0.0.1:1234/api")
        return JsonResponse(response.json(), json_dumps_params={'ensure_ascii': False})
    else:
        return render(request, "main/index.html", {})