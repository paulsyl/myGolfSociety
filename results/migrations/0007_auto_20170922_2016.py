# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 20:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20170922_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_player_link',
            name='user',
        ),
        migrations.AlterField(
            model_name='results',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User_Player_Link',
        ),
    ]