# Generated by Django 2.2 on 2020-07-18 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20200704_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
