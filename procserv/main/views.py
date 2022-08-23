from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import xmltodict
from bson import json_util
import re
from .utils import get_db_handle

class storeXML(APIView):

    def __init__(self):
        self.db_handle = get_db_handle()


    def parse_category(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'reflink': item['Ссылка'],
                        'name': item['Наименование'],
                        'parent': item['Родитель']
                    }
                )
            return result

        return {
            'reflink': data['Ссылка'],
            'name': data['Наименование'],
            'parent': data['Родитель']
        }


    def parse_measureunit(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'reflink': item['Строка']['Ссылка'],
                        'name': item['Строка']['Наименование'],
                        'full_name': item['Строка']['НаименованиеПолное']
                    }
                )
            return result

        return {
            'reflink': data['Строка']['Ссылка'],
            'name': data['Строка']['Наименование'],
            'full_name': data['Строка']['НаименованиеПолное']
        }


    def parse_product(self, data):
        if isinstance(data, list):
            result = []
            for item in data:
                result.append(
                    {
                        'reflink': item['Ссылка'],
                        'category': item['Родитель'],
                        'code': item['Артикул'],
                        'name': item['Наименование'],
                        'description': item['Описание'],
                        'product_type': 0 if item['ТипНоменклатуры'] == 'Товар' else 1,
                        'rate_nds': int(re.sub('%', '', item['СтавкаНДС'])),
                        'measure_unit': item['ЕдиницаХраненияОстатков'],
                        'hidden': int(item['ПометкаУдаления'])
                    }
                )
            return result

        return {
            'reflink': data['Ссылка'],
            'category': data['Родитель'],
            'code': data['Артикул'],
            'name': data['Наименование'],
            'description': data['Описание'],
            'product_type': 0 if data['ТипНоменклатуры'] == 'Товар' else 1,
            'rate_nds': int(re.sub('%', '', data['СтавкаНДС'])),
            'measure_unit': data['ЕдиницаХраненияОстатков'],
            'hidden': int(data['ПометкаУдаления'])
        }


    def to_mongo(self, data, col):
        col_handle = self.db_handle[col]
        upd = {'$set': {'sent': 0}}

        if isinstance(data, list):
            col_handle.insert_many(data)
            col_handle.update_many({}, upd, upsert=True)
        else:
            col_handle.insert_one(data)
            col_handle.update_one({}, upd, upsert=True)


    def post(self, request):
        xml = request.body
        raw = xmltodict.parse(xml)
        body = raw['AgoraMessage']

        if 'ГруппаНоменклатура' in body:
            data = body['ГруппаНоменклатура']
            parsed = self.parse_category(data)
            self.to_mongo(parsed, 'category')

        if 'ЕдиницыИзмерения' in body:
            data = body['ЕдиницыИзмерения']
            parsed = self.parse_measureunit(data)
            self.to_mongo(parsed, 'measure_unit')
            
        if 'Номенклатура' in body:
            data = body['Номенклатура']
            parsed = self.parse_product(data)
            self.to_mongo(parsed, 'product')

        return JsonResponse({'status': 'ok'})


class loadToMP(APIView):

    def __init__(self):
        self.db_handle = get_db_handle()


    def to_mp(self, col):
        col_handle = self.db_handle[col]
        docs = col_handle.find({'sent': 0})

        # if len(list(docs)) == 0: return 'up-to-date'

        for item in docs:
            r = requests.post(
                f'http://127.0.0.1:8000/api/{col}/',
                data=json_util.dumps(item)
            )
            if r.status_code != 200:
                return 'failed'

            col_handle.update_one(
                {'_id': item['_id']},
                {'$set': {'sent': 1}}
            )
        
        return 'ok'


    def get(self, request):

        resp = {
            'category': self.to_mp('category'),
            'measure_unit': self.to_mp('measure_unit'),
            'product': self.to_mp('product')
        }
    
        return JsonResponse(resp)

