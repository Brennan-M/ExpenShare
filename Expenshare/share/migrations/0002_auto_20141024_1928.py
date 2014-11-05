# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='groupRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='share.PayGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='contested',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='contestedMessage',
            field=models.CharField(default=b'', max_length=140),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='date',
            field=models.DateField(default=b'1995-04-04'),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='description',
            field=models.CharField(default=b'', max_length=400),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='group',
            field=models.ForeignKey(to='share.PayGroup'),
        ),
    ]
