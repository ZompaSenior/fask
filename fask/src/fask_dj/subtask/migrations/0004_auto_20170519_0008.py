# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 00:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtask', '0003_auto_20170510_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='completed_on',
            field=models.DateField(blank=True, help_text='When sub task was completed', null=True, verbose_name='Completed Date'),
        ),
    ]
