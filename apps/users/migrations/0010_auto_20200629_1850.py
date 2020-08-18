# Generated by Django 3.0.7 on 2020-06-29 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_subscribe_hours_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_partner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='parent_referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='referral_code',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
