# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 20:26
from __future__ import unicode_literals

import apps.sitio_mapa.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio_mapa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitiomapa',
            name='imagen',
            field=models.ImageField(default=1, upload_to=apps.sitio_mapa.models.upload_location),
            preserve_default=False,
        ),
    ]
