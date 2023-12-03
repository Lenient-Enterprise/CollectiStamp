# Generated by Django 4.2.7 on 2023-12-03 11:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Criterio',
                'verbose_name_plural': 'Criterios',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('stock_amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='La cantidad no puede ser negativa.'), django.core.validators.MaxValueValidator(limit_value=999, message='La cantidad no puede ser mayor que 999.')])),
                ('product_type', models.CharField(choices=[('COIN', 'Moneda'), ('SEAL', 'Sello')], max_length=10)),
                ('category', models.CharField(choices=[('ANCIENT', 'Antiguo'), ('COMIC_BOOK', 'Comic'), ('VIDEOGAME', 'Videojuego'), ('HISTORICAL', 'Histórico'), ('NOVELTY', 'Novedad')], max_length=15)),
                ('image', models.ImageField(upload_to='static/img/product/')),
                ('criteria', models.ManyToManyField(to='product.criteria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
