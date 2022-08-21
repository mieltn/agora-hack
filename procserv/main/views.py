from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json
import xmltodict
import pymongo
from bson import json_util


def get_db_handle():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db_handle = client["erp"]
    return db_handle


class XMLstore(APIView):

    def post(self, request):
        xml = request.body
        data = xmltodict.parse(xml)
        body = data['AgoraMessage']

        db_handle = get_db_handle()

        if 'ГруппаНоменклатура' in body:
            col_handle = db_handle['category']
            col_handle.drop()
            for item in body['ГруппаНоменклатура']:
                col_handle.insert_one(item)
                
        if 'ЕдиницыИзмерения' in body:
            col_handle.drop()
            col_handle = db_handle['measureunit']
            item = body['ЕдиницыИзмерения']['Строка']
            col_handle.insert_one(item)
                
        if 'Номенклатура' in body:
            col_handle.drop()
            col_handle = db_handle['product']
            for item in body['Номенклатура']:
                col_handle.insert_one(item)

        return JsonResponse({'status': 'ok'})


class dataGet(APIView):

    def get(self, request):

        print("entering get...")

        db_handle = get_db_handle()

        col_handle = db_handle['category']

        for item in col_handle.find():
            print(item)
            r = requests.post(
                "http://127.0.0.1:8000/api/category/",
                data=json_util.dumps(item)
            )
            if r.status_code != 200:
                return JsonResponse({'status': 'failed'})


        col_handle = db_handle['measureunit']
        for item in col_handle.find():
            r = requests.post(
                "http://127.0.0.1:8000/api/measureunit/",
                data=json_util.dumps(item)
            )
            if r.status_code != 200:
                return JsonResponse({'status': 'failed'})


        col_handle = db_handle['product']
        for item in col_handle.find():
            r = requests.post(
                "http://127.0.0.1:8000/api/product/",
                data=json_util.dumps(item)
            )
            if r.status_code != 200:
                return JsonResponse({'status': 'failed'})

        return JsonResponse({'status': 'ok'})

