# Generated by Django 3.0.7 on 2020-06-19 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_houseinfo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='houseinfo',
            name='house',
        ),
        migrations.AddField(
            model_name='housemodel',
            name='house_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.HouseInfo'),
        ),
    ]
