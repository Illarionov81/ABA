# Generated by Django 3.1.5 on 2021-01-18 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20201225_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programskill',
            name='status',
        ),
    ]
