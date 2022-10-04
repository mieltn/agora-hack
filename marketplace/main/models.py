from django.db import models

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    categoryId = models.CharField(max_length=50, primary_key=True)
    parent = TreeForeignKey(
        'self',
        blank = True,
        null = True,
        verbose_name = 'Родительская категория',
        related_name = 'child',
        on_delete = models.CASCADE
    )
    name = models.CharField(max_length=550)
    
    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'


class MeasureUnit(models.Model):
    measureUnitId = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    full_name = models.CharField(max_length=255, blank=True, default='',verbose_name='Полное название')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Product(models.Model):

    PRODUCT = 0
    SERVICE = 1

    TYPES = (
        (PRODUCT, 'Товар'),
        (SERVICE, 'Услуга'),
    )

    productId = models.CharField(max_length=50, primary_key=True)
    category = TreeForeignKey(
        Category,
        null = True,
        blank = True,
        related_name = 'products',
        on_delete = models.SET_NULL,
        verbose_name = 'Категория'
    )
    code = models.CharField(max_length=255, verbose_name='Артикул', blank=True, null=True, default='')
    name = models.CharField(max_length=1024, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    product_type = models.IntegerField(choices=TYPES, default=PRODUCT, verbose_name='Тип номенклатуры')
    rate_nds = models.FloatField(default=20, verbose_name='Ставка НДС')
    measure_unit = models.ForeignKey(
        MeasureUnit,
        null = True,
        blank = True,
        verbose_name = 'Единица измерения',
        on_delete = models.SET_NULL
    )
    hidden = models.BooleanField(default=False, verbose_name='Скрывать товар в Agora', db_index=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
