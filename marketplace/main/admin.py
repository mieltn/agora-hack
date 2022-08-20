from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, MeasureUnit, Product

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(MeasureUnit)
admin.site.register(Product)