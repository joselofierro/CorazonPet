# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20171201_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='contrasena',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
