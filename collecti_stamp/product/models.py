from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.TextChoices):

    ANCIENT = 'ANCIENT', 'Antiguo'
    COMIC_BOOK = 'COMIC_BOOK', 'Comic'
    VIDEOGAME = 'VIDEOGAME', 'Videojuego'
    HISTORICAL = 'HISTORICAL', 'Histórico'
    NOVELTY = 'NOVELTY', 'Novedad'


class Criteria(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Criterio"
        verbose_name_plural = "Criterios"

    def __str__(self):
        return self.name


class ProductType(models.TextChoices):
    COIN = 'COIN', 'Moneda'
    SEAL = 'SEAL', 'Sello'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_amount = models.IntegerField(validators=[
            MinValueValidator(limit_value=0, message='La cantidad no puede ser negativa.'),
            MaxValueValidator(limit_value=999, message='La cantidad no puede ser mayor que 999.'),
    ])
    product_type = models.CharField(max_length=10, choices=ProductType.choices)
    category = models.CharField(max_length=15, choices=Category.choices)
    criteria = models.ManyToManyField(Criteria)
    image = models.ImageField(upload_to='static/img/product/')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name
