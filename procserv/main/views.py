from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json
import xmltodict


class XMLexchange(APIView):

    def get(self, request):
        r = requests.get("http://127.0.0.1:5678/api/")
        if r.status_code == 200:
            return JsonResponse({'status': 'ok'})

        return JsonResponse({'status': 'failed'})


    def post(self, request):
        xml = request.body
        data = xmltodict.parse(xml)
        body = data['AgoraMessage']

        if 'ГруппаНоменклатура' in body:
            for item in body['ГруппаНоменклатура']:
                r = requests.post("http://127.0.0.1:8000/api/category/", data=json.dumps(item))
                if r.status_code != 200:
                    return JsonResponse({'status': 'failed'})
    

        if 'ЕдиницыИзмерения' in body:
            item = body['ЕдиницыИзмерения']['Строка']
            r = requests.post("http://127.0.0.1:8000/api/measureunit/", data=json.dumps(item))
            if r.status_code != 200:
                return JsonResponse({'status': 'failed'})
                

        if 'Номенклатура' in body:
            for item in body['Номенклатура']:
                r = requests.post("http://127.0.0.1:8000/api/product/", data=json.dumps(item))
                if r.status_code != 200:
                    return JsonResponse({'status': 'failed'})

        return JsonResponse({'status': 'ok'})



