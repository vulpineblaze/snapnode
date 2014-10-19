# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160)),
                ('desc', models.TextField(max_length=1600)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name=b'date updated')),
                ('parent', models.ForeignKey(to='core.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
