# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mascota_premium', '0002_auto_20171205_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascotapremium',
            name='mascota',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mascota_premium', to='mascota.Mascota'),
        ),
    ]
