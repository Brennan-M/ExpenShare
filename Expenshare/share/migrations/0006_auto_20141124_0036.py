# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0005_auto_20141123_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='FellowUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owed', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('netOwed', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('fellows', models.ManyToManyField(to='share.FellowUser')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paygroup',
            name='memberViews',
            field=models.ManyToManyField(to='share.MemberView'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paygroup',
            name='description',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='paygroup',
            name='name',
            field=models.CharField(default=b'', unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='amount',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='date',
            field=models.DateField(default=b'2014-11-24'),
        ),
        migrations.AlterField(
            model_name='paymentlog',
            name='description',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
