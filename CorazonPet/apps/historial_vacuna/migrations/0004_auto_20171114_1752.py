# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial_vacuna', '0003_auto_20171114_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialvacuna',
            name='prioridad',
            field=models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], max_length=10),
        ),
    ]
