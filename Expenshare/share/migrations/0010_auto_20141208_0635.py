# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0009_auto_20141207_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlog',
            name='date',
            field=models.DateField(default=b'2014-12-08'),
            preserve_default=True,
        ),
    ]
