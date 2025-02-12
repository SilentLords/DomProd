# Generated by Django 3.0.7 on 2020-08-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_user_all_discount_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_to_add', models.IntegerField(default=0)),
                ('limit_of_activations', models.IntegerField(default=0)),
                ('code', models.IntegerField(max_length=20)),
            ],
        ),
    ]
