# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20171212_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='ciudad',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='ciudad.Ciudad'),
        ),
    ]