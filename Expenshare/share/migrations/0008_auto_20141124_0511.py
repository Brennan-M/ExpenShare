# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0007_paygroup_groupsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paygroup',
            name='groupSize',
            field=models.IntegerField(default=1),
        ),
    ]
