# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-18 22:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('historial_vacuna', '0009_historialvacuna_vacuna_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialvacuna',
            name='imagen',
        ),
    ]
