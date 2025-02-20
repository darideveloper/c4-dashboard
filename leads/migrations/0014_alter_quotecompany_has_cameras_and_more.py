# Generated by Django 4.2.7 on 2025-02-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_quotecompany_has_cameras_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotecompany',
            name='has_cameras',
            field=models.CharField(choices=[('yes', 'Sí, solo quiero monitoreo'), ('no', 'No, quiero instalación también'), ('maintenance', 'Solo quiero mantenimiento')], max_length=20, verbose_name='tiene cámaras'),
        ),
        migrations.AlterField(
            model_name='quoteresidential',
            name='has_cameras',
            field=models.CharField(choices=[('yes', 'Sí, solo quiero monitoreo'), ('no', 'No, quiero instalación también')], max_length=20, verbose_name='tiene cámaras'),
        ),
    ]
