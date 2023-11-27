# company/models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_phone = models.TextField()
    contact_email = models.TextField()
    description = models.TextField()
    logo = models.ImageField(upload_to='static/img/company/')
    cif = models.CharField(max_length=255)

    def __str__(self):
        return self.name

