# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recordatorio', '0009_auto_20171220_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identificadorrecordatorio',
            name='recordatorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identificadores', to='recordatorio.Recordatorio'),
        ),
    ]
