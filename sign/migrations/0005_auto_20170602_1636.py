# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-02 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0004_auto_20170601_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='market_goods',
            name='quality',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='my_goods',
            name='quality',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
