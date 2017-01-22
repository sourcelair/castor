# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DockerServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(default='auto', max_length=255)),
                ('docker_host', models.CharField(max_length=255)),
                ('docker_tls_verify', models.BooleanField(default=True)),
                ('docker_cert_path', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
