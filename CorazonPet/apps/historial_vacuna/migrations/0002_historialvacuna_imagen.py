# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 14:50
from __future__ import unicode_literals

import apps.historial_vacuna.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial_vacuna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialvacuna',
            name='imagen',
            field=models.ImageField(default=1, upload_to=apps.historial_vacuna.models.upload_location),
            preserve_default=False,
        ),
    ]
