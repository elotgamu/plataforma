# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 18:09
from __future__ import unicode_literals

from django.db import migrations, models
import publicidad.models


class Migration(migrations.Migration):

    dependencies = [
        ('publicidad', '0006_category_negocio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negocio',
            name='menu_path',
            field=models.FileField(blank=True, null=True, upload_to=publicidad.models.menu_upload_to),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='flyer',
            field=models.ImageField(upload_to='promotions/%Y_%m_%d/'),
        ),
    ]
