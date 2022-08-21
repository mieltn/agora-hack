from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
import requests
import json
import re
from .models import Product, Category, MeasureUnit
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.method == "POST":
        response = requests.get("http://127.0.0.1:1234/api/dataget/")
        return JsonResponse(response.json(), json_dumps_params={'ensure_ascii': False})
    else:
        return render(request, "main/index.html", {})


@csrf_exempt
def newCategory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            parent = Category.objects.get(parent=data['Родитель'])
        except:
            parent = None

        newcat = Category(
            parent = parent,
            name = data['Наименование'],
            reflink = data['Ссылка']
            # parentref = data['Родитель']
        )
        newcat.save()
        print(newcat.pk)
        # return HttpResponseRedirect(reverse('index'))
        return JsonResponse(data)


@csrf_exempt
def newMeasureUnit(request):
    data = json.loads(request.body)
    newmu = MeasureUnit(
        name = data['Наименование'],
        full_name = data['НаименованиеПолное'],
        reflink = data['Ссылка']
    )
    newmu.save()
    # return HttpResponseRedirect(reverse('index'))
    return JsonResponse(data)


@csrf_exempt
def newProduct(request):
    data = json.loads(request.body)
    try:
        category = Category.objects.get(reflink=data['Родитель'])
    except:
        category = None

    mu = MeasureUnit.objects.get(reflink=data['ЕдиницаХраненияОстатков'])

    if data['ТипНоменклатуры'] == 'Товар':
        pt = 0
    elif data['ТипНоменклатуры'] == 'Услуга':
        pt = 1

    product = Product(
        category = category,
        code = data['Артикул'],
        name = data['Наименование'],
        description = data['Описание'],
        product_type = pt,
        rate_nds = int(re.sub('%', '', data['СтавкаНДС'])),
        measure_unit = mu,
        hidden = data['ПометкаУдаления'],
        reflink = data['Ссылка'],
        # parentref = data['Родитель'],
        
    )
    product.save()
    # return HttpResponseRedirect(reverse('index'))
    return JsonResponse(data)
