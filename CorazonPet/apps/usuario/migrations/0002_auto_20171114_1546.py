# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='idFacebook',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]