# Generated by Django 3.2 on 2022-09-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220906_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
            ],
        ),
    ]
