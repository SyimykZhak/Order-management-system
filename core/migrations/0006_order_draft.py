# Generated by Django 4.0.5 on 2022-06-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_order_name_alter_order_order_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Черновик'),
        ),
    ]
