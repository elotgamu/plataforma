# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negocios_publicidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/default.jpg', null=True, upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/default.jpg', null=True, upload_to='profiles/'),
        ),
    ]