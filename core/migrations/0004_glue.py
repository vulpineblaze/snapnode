# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name=b'date updated')),
                ('child', models.ForeignKey(related_name=b'node_child', to='core.Node')),
                ('parent', models.ForeignKey(related_name=b'node_parent', to='core.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
