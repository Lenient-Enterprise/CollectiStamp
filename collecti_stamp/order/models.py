from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from product.models import *


class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'CASH_ON_DELIVERY', 'Contrarrembolso'
    PAYMENT_GATEWAY = 'PAYMENT_GATEWAY', 'Pasarelas de Pago'


class DeliveryStatus(models.TextChoices):
    STATUS_A = 'A', 'A'
    STATUS_B = 'B', 'B'
    STATUS_C = 'C', 'C'


class DeliveryMethod(models.TextChoices):
    STANDARD_SHIPPING = 'STD', 'Envío estándar'
    EXPRESS_SHIPPING = 'EXP', 'Envío express'
    PICKUP_IN_STORE = 'PICK', 'Recogida en tienda'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=50)
    order_date = models.DateField()
    order_total = models.DecimalField(max_digits=7, decimal_places=2)
    order_is_finished = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    delivery_status = models.CharField(max_length=20, choices=DeliveryStatus.choices)
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethod.choices)
    delivery_cost = models.DecimalField(max_digits=7, decimal_places=2)
    delivery_address = models.TextField(max_length=500)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return "Compra " + str(self.id)


class OrderProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ManyToManyField(Order)
    product_id = models.ManyToManyField(Product)
    quantity = models.IntegerField(validators=[
            MinValueValidator(limit_value=0, message='La cantidad no puede ser negativa.'),
            MaxValueValidator(limit_value=999, message='La cantidad no puede ser mayor que 999.'),
    ])

    class Meta:
        verbose_name = "Producto de compra"
        verbose_name_plural = "Productos de compra"
