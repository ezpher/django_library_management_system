# Generated by Django 2.2 on 2020-08-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200718_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='books',
            field=models.ManyToManyField(blank=True, through='main.BookTransaction', to='main.Book'),
        ),
    ]