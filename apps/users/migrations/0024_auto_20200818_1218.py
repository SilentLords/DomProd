# Generated by Django 3.0.7 on 2020-08-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_discountcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='code',
            field=models.CharField(max_length=20),
        ),
    ]
