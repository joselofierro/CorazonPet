# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 19:01
from __future__ import unicode_literals

import apps.mascota.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='foto_perfil',
            field=models.ImageField(default=1, upload_to=apps.mascota.models.upload_location),
            preserve_default=False,
        ),
    ]
