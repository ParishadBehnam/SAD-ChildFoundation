# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-21 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='information',
            options={'verbose_name': 'اطلاع کلان سامانه', 'verbose_name_plural': 'اطلاعات کلان سامانه'},
        ),
        migrations.AlterField(
            model_name='information',
            name='activities',
            field=models.TextField(verbose_name='فعالیت\u200cها'),
        ),
        migrations.AlterField(
            model_name='information',
            name='chart',
            field=models.CharField(max_length=30, verbose_name='چارت سازمانی'),
        ),
        migrations.AlterField(
            model_name='information',
            name='goals',
            field=models.TextField(verbose_name='اهداف'),
        ),
        migrations.AlterField(
            model_name='information',
            name='history',
            field=models.TextField(primary_key=True, serialize=False, verbose_name='تاریخچه'),
        ),
        migrations.AlterField(
            model_name='information',
            name='supporters',
            field=models.TextField(verbose_name='حمایت\u200cکننده\u200cها'),
        ),
    ]
