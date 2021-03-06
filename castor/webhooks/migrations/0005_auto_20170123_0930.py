# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 09:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0004_auto_20170123_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='failure_reason',
            field=models.TextField(blank=True, default='', max_length=65535),
        ),
        migrations.AlterField(
            model_name='notification',
            name='request_body',
            field=models.TextField(blank=True, default='', max_length=65535),
        ),
        migrations.AlterField(
            model_name='notification',
            name='request_headers',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='notification',
            name='response_body',
            field=models.TextField(blank=True, default='', max_length=65535),
        ),
        migrations.AlterField(
            model_name='notification',
            name='response_headers',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
