from django.db import models
from product.models import Product


# Create your models here.
class Claim(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, default="Anónimo")
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reclamación"
        verbose_name_plural = "Reclamaciones"

    def __str__(self):
        return self.title