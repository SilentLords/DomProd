# Generated by Django 3.0.7 on 2020-06-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200629_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='referral_code',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]