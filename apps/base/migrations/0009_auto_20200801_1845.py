# Generated by Django 3.0.7 on 2020-08-01 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_merge_20200718_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='houseinfo',
            name='land_area',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='housemodel',
            name='parsing_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='creation_time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housemodel',
            name='x_cord',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='housemodel',
            name='y_cord',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='city',
            field=models.CharField(blank=True, choices=[(0, 'Тюмень')], max_length=20, null=True),
        ),
    ]
