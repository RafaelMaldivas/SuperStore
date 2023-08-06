# Generated by Django 4.2.4 on 2023-08-06 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='descricao',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
