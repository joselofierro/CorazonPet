# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mascota', '0001_initial'),
        ('medicamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialMedico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosis', models.CharField(max_length=20)),
                ('observacion', models.CharField(max_length=100)),
                ('mascota', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mascota.Mascota')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicamento.Medicamento')),
            ],
        ),
    ]