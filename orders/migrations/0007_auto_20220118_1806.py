# Generated by Django 3.1 on 2022-01-19 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20220112_2206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='variation',
            new_name='variations',
        ),
    ]