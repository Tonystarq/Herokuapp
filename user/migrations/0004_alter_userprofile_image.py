# Generated by Django 3.2 on 2022-09-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220906_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/'),
        ),
    ]
