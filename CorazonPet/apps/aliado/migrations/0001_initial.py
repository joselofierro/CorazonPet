# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 21:01
from __future__ import unicode_literals

import apps.aliado.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aliado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descuento', models.IntegerField()),
                ('observacion', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(upload_to=apps.aliado.models.upload_location)),
            ],
        ),
    ]
