# Generated by Django 3.1 on 2022-01-13 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20220112_2004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='orders',
            new_name='order',
        ),
    ]