# Generated by Django 5.0.3 on 2024-04-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
