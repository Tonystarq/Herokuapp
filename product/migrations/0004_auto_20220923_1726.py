# Generated by Django 3.2 on 2022-09-23 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discountedPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='variants',
            name='discountedPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
