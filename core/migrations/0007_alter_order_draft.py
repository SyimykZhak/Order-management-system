# Generated by Django 4.0.5 on 2022-06-27 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_order_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Сделано'),
        ),
    ]
