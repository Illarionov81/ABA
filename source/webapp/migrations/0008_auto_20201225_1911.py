# Generated by Django 2.2.13 on 2020-12-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_merge_20201221_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prorgamskillgoal',
            name='goal',
            field=models.CharField(default='', max_length=1000, null=True, verbose_name='Дополнительная цель'),
        ),
    ]
