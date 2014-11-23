# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0004_auto_20141123_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paygroup',
            name='description',
            field=models.CharField(default=b'', max_length=140),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='description',
            field=models.CharField(default=b'', max_length=140),
        ),
    ]
