# Generated by Django 4.0.3 on 2022-06-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0016_shippingaddress_freeshipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='is_stopdesk',
            field=models.BooleanField(default=True),
        ),
    ]