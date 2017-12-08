# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordatorio', '0002_auto_20171127_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordatorio',
            name='actividad',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='domingo',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='jueves',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='lunes',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='martes',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='miercoles',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='sabado',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recordatorio',
            name='viernes',
            field=models.NullBooleanField(default=False),
        ),
    ]