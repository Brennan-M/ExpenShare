# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0006_auto_20141124_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='paygroup',
            name='groupSize',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
