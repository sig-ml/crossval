# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20160825_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='metric',
            field=models.CharField(default='accuracy', max_length=50),
        ),
    ]
