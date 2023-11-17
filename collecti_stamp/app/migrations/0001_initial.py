# Generated by Django 4.2.5 on 2023-11-12 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('ticket_date', models.DateTimeField()),
                ('status', models.CharField(default='Not Used', max_length=50)),
                ('finish_date', models.DateTimeField()),
                ('last_used', models.DateTimeField(blank=True, null=True)),
                ('type_ticket', models.CharField(default='Day', max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-ticket_date'],
            },
        ),
    ]