# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0003_auto_20141024_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payGroups', models.ManyToManyField(to='share.PayGroup')),
                ('userKey', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='grouprequest',
            name='group',
        ),
        migrations.RemoveField(
            model_name='grouprequest',
            name='user',
        ),
        migrations.DeleteModel(
            name='groupRequest',
        ),
        migrations.RemoveField(
            model_name='paymentlog',
            name='group',
        ),
        migrations.AddField(
            model_name='paygroup',
            name='paymentLogs',
            field=models.ManyToManyField(to='share.PaymentLog'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paygroup',
            name='name',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='date',
            field=models.DateField(default=b'2014-11-23'),
        ),
    ]
