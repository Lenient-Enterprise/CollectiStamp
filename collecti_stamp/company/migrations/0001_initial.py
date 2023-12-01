from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('contact_phone', models.TextField()),
                ('contact_email', models.TextField()),
                ('description', models.TextField()),
                ('logo', models.ImageField(upload_to='static/img/company/')),
                ('cif', models.CharField(max_length=255)),
            ],
        ),
    ]
