from doctest import DocFileSuite
from django.shortcuts import render
from django.http import JsonResponse
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
        item = json.loads(request.body)

        try:
            parent = Category.objects.get(reflink=item['parent'])
        except Category.DoesNotExist:
            parent = None
            
        ct, created = Category.objects.get_or_create(
            reflink = item['reflink'],
            name = item['name'],
            parent = parent
        )
        if created: ct.save()
        return JsonResponse({'ct': ct.reflink})


@csrf_exempt
def newMeasureUnit(request):
    item = json.loads(request.body)
    mu, created = MeasureUnit.objects.get_or_create(
        reflink = item['reflink'],
        name = item['name'],
        full_name = item['full_name']
    )
    if created: mu.save()
    return JsonResponse({'mu': mu.reflink})


@csrf_exempt
def newProduct(request):
    item = json.loads(request.body)

    pr, created = Product.objects.get_or_create(
        reflink = item['reflink'],
        category_id = item['category'],
        code = item['code'],
        name = item['name'],
        description = item['description'],
        product_type = item['product_type'],
        rate_nds = item['rate_nds'],
        measure_unit_id = item['measure_unit'],
        hidden = item['hidden']        
    )
    if created: pr.save()
    return JsonResponse({'pr': pr.reflink})
