# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-01 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('active_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='removed_sponsership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('hamyar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='active_user.hamyar')),
                ('madadjoo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='active_user.madadjoo')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='removed_sponsership',
            unique_together=set([('madadjoo', 'hamyar')]),
        ),
    ]
