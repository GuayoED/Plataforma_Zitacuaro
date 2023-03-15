# Generated by Django 4.1.1 on 2022-12-08 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciclaje', '0010_puntosreciclaje_alter_user_options_entradas_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispofinal',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entradas',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dispofinal',
            name='nombre',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='entradas',
            name='fecha',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='puntos',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]