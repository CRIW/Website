# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campusradio', '0004_auto_20170217_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='mp3_link',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
