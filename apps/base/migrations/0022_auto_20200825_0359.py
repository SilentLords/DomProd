# Generated by Django 3.0.7 on 2020-08-25 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20200825_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housemodel',
            name='city',
            field=models.IntegerField(blank=True, choices=[(0, 'Тюмень')], max_length=20, null=True),
        ),
    ]
