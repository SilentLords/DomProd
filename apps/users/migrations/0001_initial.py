# Generated by Django 3.0.7 on 2020-06-15 17:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed. ", regex='^\\+?1?\\d{9,14}$')])),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('surname', models.CharField(blank=True, max_length=40, null=True)),
                ('subscribe_trial', models.BooleanField(default=True)),
                ('subscribe', models.BooleanField(default=False)),
                ('subscribe_start_time', models.DateTimeField()),
                ('subscribe_days_count', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField()),
                ('fav_list', models.ManyToManyField(related_name='fav_list', to='apis.HouseModel')),
                ('ignore_list', models.ManyToManyField(related_name='ignore_list', to='apis.HouseModel')),
                ('watched_list', models.ManyToManyField(related_name='watched_list', to='apis.HouseModel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
