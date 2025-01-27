# Generated by Django 3.0.7 on 2020-06-30 21:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200622_1349'),
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
        migrations.AddField(
            model_name='user',
            name='subscribe_hours_count',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=0)),
                ('payment_id', models.CharField(max_length=60)),
                ('is_success', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
