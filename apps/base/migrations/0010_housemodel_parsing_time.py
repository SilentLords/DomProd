# Generated by Django 3.0.7 on 2020-07-18 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20200714_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemodel',
            name='parsing_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
