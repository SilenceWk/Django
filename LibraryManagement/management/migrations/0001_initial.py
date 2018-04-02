# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='社团名称', max_length=128)),
                ('price', models.IntegerField(verbose_name='社团人数')),
                ('author', models.CharField(verbose_name='社长', max_length=128)),
                ('publish_date', models.DateField(verbose_name='社团成立日期')),
                ('category', models.CharField(verbose_name='社团类别', max_length=128)),
                ('detail', models.CharField(verbose_name='社团描述', max_length=255)),
            ],
            options={
                'db_table': 'management_book',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='club_zixun',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('aid', models.IntegerField()),
                ('activity_name', models.CharField(max_length=50)),
                ('activity_describe', models.CharField(max_length=200)),
                ('activity_person', models.IntegerField()),
                ('activity_img', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'club_zixun',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('img', models.ImageField(upload_to='image/%Y/%m/%d/')),
                ('book', models.ForeignKey(to='management.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Myadmin',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'myadmin',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uid', models.IntegerField(max_length=11)),
                ('nickname', models.CharField(max_length=16)),
                ('permission', models.IntegerField(default=1)),
                ('user_state', models.IntegerField(default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
