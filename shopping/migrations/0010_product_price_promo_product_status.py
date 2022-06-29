# Generated by Django 4.0.3 on 2022-06-20 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0009_affaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_promo',
            field=models.FloatField(blank=True, null=True, verbose_name='prix de promotion'),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]