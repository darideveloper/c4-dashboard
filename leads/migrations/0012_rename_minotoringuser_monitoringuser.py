# Generated by Django 4.2.7 on 2024-12-26 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_minotoringuser_monitoringtarget_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MinotoringUser',
            new_name='MonitoringUser',
        ),
    ]