from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .serializers import ProductSerializer, CategorySerializer, MeasureUnitSerializer

import requests


class Upload(APIView):

    # for localhost
    # URL = 'http://0.0.0.0:2000/senddata/'
    # for docker
    URL = 'http://agora-hack-procserv-1:2000/senddata/'

    def get(self, request):
        response = requests.get(self.URL)
        return JsonResponse(
            response.json(),
            status = status.HTTP_200_OK
        )
        

class Products(APIView):

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Categories(APIView):

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasureUnits(APIView):

    def post(self, request):
        serializer = MeasureUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
