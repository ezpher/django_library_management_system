# Generated by Django 2.2 on 2020-06-24 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_transaction_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='test',
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_ref',
            field=models.CharField(default='T000-0000-000', max_length=13, unique=True),
        ),
    ]
