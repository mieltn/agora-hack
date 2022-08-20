from rest_framework.views import APIView
from django.http import JsonResponse
import xmltodict

class XMLget(APIView):
    def get(self, request):
        with open("case_2_input_data.xml", "r", encoding="utf-8") as f:
            o = f.read()
            data = xmltodict.parse(o)
            return JsonResponse(data)
