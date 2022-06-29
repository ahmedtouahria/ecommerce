# Generated by Django 4.0.3 on 2022-06-11 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_conversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.variation'),
        ),
        migrations.AddField(
            model_name='variation',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]