from rest_framework.views import APIView
from django.http import JsonResponse
import requests

class XMLsend(APIView):
    def get(self, request):
        with open("main/case_3_input_data.xml", "r") as f:
            xmlstr = f.read()
            headers = {'Content-Type': 'application/xml'}
            r = requests.post("http://127.0.0.1:1234/api/", data=xmlstr.encode('utf-8'), headers=headers)

            if r.status_code == 200:
                return JsonResponse({'status': 'ok'})

            return JsonResponse({'status': 'failed'})