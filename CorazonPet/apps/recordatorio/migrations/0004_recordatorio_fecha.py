# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordatorio', '0003_auto_20171128_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordatorio',
            name='fecha',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
