# Generated by Django 4.2.4 on 2023-10-14 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_endereco_order_logradouro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='pagamento_method',
            field=models.CharField(default='PIX', max_length=100),
        ),
    ]