from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

import xmltodict
from bson import json_util
import re

import requests

import time

from .utils import getDBHandle


class UploadXML(APIView):

    DBHandle = getDBHandle()

    def parseCategory(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'categoryId': item['Ссылка'],
                        'name': item['Наименование'],
                        'parent': None if item['Родитель'] == item['Ссылка'] else item['Родитель'],
                        'sent': 0
                    }
                )
            return result

        return {
            'categoryId': data['Ссылка'],
            'name': data['Наименование'],
            'parent': data['Родитель'],
            'sent': 0
        }


    def parseMeasureUnit(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'measureUnitId': item['Строка']['Ссылка'],
                        'name': item['Строка']['Наименование'],
                        'full_name': item['Строка']['НаименованиеПолное'],
                        'sent': 0
                    }
                )
            return result

        return {
            'measureUnitId': data['Строка']['Ссылка'],
            'name': data['Строка']['Наименование'],
            'full_name': data['Строка']['НаименованиеПолное'],
            'sent': 0
        }


    def parseProduct(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'productId': item['Ссылка'],
                        'category': item['Родитель'],
                        'code': item['Артикул'],
                        'name': item['Наименование'],
                        'description': item['Описание'],
                        'product_type': 0 if item['ТипНоменклатуры'] == 'Товар' else 1,
                        'rate_nds': int(re.sub('%', '', item['СтавкаНДС'])),
                        'measure_unit': item['ЕдиницаХраненияОстатков'],
                        'hidden': int(item['ПометкаУдаления']),
                        'sent': 0
                    }
                )
            return result

        return {
            'productId': data['Ссылка'],
            'category': data['Родитель'],
            'code': data['Артикул'],
            'name': data['Наименование'],
            'description': data['Описание'],
            'product_type': 0 if data['ТипНоменклатуры'] == 'Товар' else 1,
            'rate_nds': int(re.sub('%', '', data['СтавкаНДС'])),
            'measure_unit': data['ЕдиницаХраненияОстатков'],
            'hidden': int(data['ПометкаУдаления']),
            'sent': 0
        }


    def toMongo(self, data, col):
        colHandle = self.DBHandle[col]

        if isinstance(data, list):
            colHandle.insert_many(data)
            return len(data)
        
        colHandle.insert_one(data)
        return 1


    def post(self, request):
        xml = request.body
        raw = xmltodict.parse(xml)
        body = raw['AgoraMessage']

        result = {}

        startTime = time.time()

        if 'ГруппаНоменклатура' in body:
            data = body['ГруппаНоменклатура']
            parsed = self.parseCategory(data)
            cnt = self.toMongo(parsed, 'categories')
            result['categories received'] = cnt

        if 'ЕдиницыИзмерения' in body:
            data = body['ЕдиницыИзмерения']
            parsed = self.parseMeasureUnit(data)
            cnt = self.toMongo(parsed, 'measureunits')
            result['measure units received'] = cnt
            
        if 'Номенклатура' in body:
            data = body['Номенклатура']
            parsed = self.parseProduct(data)
            cnt = self.toMongo(parsed, 'products')
            result['products received'] = cnt

        timeDiff = time.time() - startTime
        result['total seconds'] = round(timeDiff, 2)

        return JsonResponse(result, status=status.HTTP_200_OK)


class SendData(APIView):

    DBHandle = getDBHandle()

    def send(self, col):
        colHandle = self.DBHandle[col]
        docs = list(colHandle.find({'sent': 0}))

        if len(docs) == 0:
            return {'status': status.HTTP_304_NOT_MODIFIED}

        for item in docs:
            response = requests.post(
                'http://127.0.0.1:3000/{}/'.format(col),
                data = json_util.dumps(item),
                headers = {'Content-Type': 'application/json'}
            )
            if response.status_code != status.HTTP_201_CREATED:
                return {'response': response.text, 'status': status.HTTP_400_BAD_REQUEST}

            colHandle.update_one(
                {'_id': item['_id']},
                {'$set': {'sent': 1}}
            )
        
        return {'items uploaded': len(docs), 'status': status.HTTP_200_OK}


    def get(self, request):

        startTime = time.time()

        response = {
            'category': self.send('categories'),
            'measureunit': self.send('measureunits'),
            'product': self.send('products')
        }

        timeDiff = time.time() - startTime
        response['total seconds'] = round(timeDiff, 2)
    
        return JsonResponse(response)
