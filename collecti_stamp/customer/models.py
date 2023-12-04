from django.contrib.auth.models import AbstractUser
from django.db import models
from order.models import PaymentMethod, DeliveryMethod


class User(AbstractUser):

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    address = models.TextField(max_length=500, blank=True, null=True, verbose_name="Dirección de Envío")
    delivery_method = models.CharField(max_length=20, null=True, choices=DeliveryMethod.choices)
    payment_method = models.CharField(max_length=20, null=True,choices=PaymentMethod.choices)

