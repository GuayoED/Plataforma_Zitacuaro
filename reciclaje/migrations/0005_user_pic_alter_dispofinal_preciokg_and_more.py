# Generated by Django 4.1.1 on 2022-11-06 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciclaje', '0004_user_remove_escuelas_user_delete_ciudadano_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pic',
            field=models.ImageField(default='unknown.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='dispofinal',
            name='preciokg',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='dispofinal',
            name='puntoskg',
            field=models.IntegerField(default=1),
        ),
    ]
