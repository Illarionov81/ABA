# Generated by Django 2.2.13 on 2020-12-17 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20201217_1944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionskill',
            options={'ordering': ['-id'], 'verbose_name': 'Навыки для отработки', 'verbose_name_plural': 'Навыки для отработки'},
        ),
    ]