# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 14:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20170930_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='age',
        ),
    ]
