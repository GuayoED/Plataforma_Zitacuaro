# Generated by Django 4.1.1 on 2023-03-23 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reciclaje', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
