# Generated by Django 3.0.7 on 2020-06-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscribe_start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
