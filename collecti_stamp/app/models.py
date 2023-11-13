# Create your models here.
import uuid

from django.db import models

from user_management.models import User


class Tickets(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # TODO: Cambiar a partir de aquí.
    title = models.CharField(max_length=100)
    description = models.TextField()
    ticket_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='Not Used')
    finish_date = models.DateTimeField()
    last_used = models.DateTimeField(null=True, blank=True)
    type_ticket = models.CharField(max_length=50, default='Day')

    def __str__(self):
        return f"Ticket UUID: {self.uuid}, Title: {self.title}, Status: {self.status}"


    class Meta:
        ordering = ['-ticket_date']
