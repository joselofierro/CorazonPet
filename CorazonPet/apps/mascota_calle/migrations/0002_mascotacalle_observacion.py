# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota_calle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascotacalle',
            name='observacion',
            field=models.CharField(default=1, max_length=140),
            preserve_default=False,
        ),
    ]
