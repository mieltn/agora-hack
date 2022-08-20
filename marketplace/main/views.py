from django.shortcuts import render
# from django.urls import reverse
from django.http import JsonResponse
import requests
import json

# Create your views here.
def index(request):
    if request.method == "POST":
        response = requests.get("http://localhost:1234")
        return JsonResponse(json.dumps(response))
    else:
        return render(request, "main/index.html", {})