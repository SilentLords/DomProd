# Generated by Django 3.0.7 on 2020-08-18 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_merge_20200807_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemodel',
            name='offer_type',
            field=models.CharField(choices=[(0, 'Купить'), (1, 'Аренда')], default=0, max_length=40),
        ),
    ]