# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0002_auto_20141024_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='paygroup',
            name='passcode',
            field=models.CharField(default=b'', max_length=16),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paygroup',
            name='description',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]
