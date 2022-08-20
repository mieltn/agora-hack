from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json


class XMLget(APIView):
    def get(self, request):
        response = requests.get("http://127.0.0.1:5678/api/")
        data = response.json()

        body = data['AgoraMessage']

        if 'ГруппаНоменклатура' in body:
            for item in body['ГруппаНоменклатура']:
                r = requests.post("http://127.0.0.1:8000/api/category/", data=json.dumps(item))
    

        if 'ЕдиницыИзмерения' in body:
            item = body['ЕдиницыИзмерения']['Строка']
            r = requests.post("http://127.0.0.1:8000/api/measureunit/", data=json.dumps(item))
                

        if 'Номенклатура' in body:
            for item in body['Номенклатура']:
                r = requests.post("http://127.0.0.1:8000/api/product/", data=json.dumps(item))

        return JsonResponse(response.json(), json_dumps_params={'ensure_ascii': False})
