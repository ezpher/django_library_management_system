# Generated by Django 2.2 on 2020-06-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_book_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='test',
            field=models.CharField(default='test', max_length=20),
        ),
    ]
