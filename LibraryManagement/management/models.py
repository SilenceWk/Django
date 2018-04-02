from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    uid = models.IntegerField(max_length=11, default=0)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)
    user_state = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Club(models.Model):
    name = models.CharField(max_length=128, verbose_name='社团名称')
    price = models.IntegerField(verbose_name='社团人数')
    author = models.CharField(max_length=128, verbose_name='社长')
    publish_date = models.DateField(verbose_name='社团成立日期')
    category = models.CharField(max_length=128, verbose_name='社团类别')
    detail = models.CharField(max_length=255, verbose_name='社团描述')


    class Meta:
        db_table = 'management_book'
        ordering = ['name']


    def __str__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Club)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name

class club_zixun(models.Model):
    aid = models.IntegerField(default=0)
    activity_name = models.CharField(max_length=50)
    activity_describe = models.CharField(max_length=200)
    activity_person = models.IntegerField()
    activity_img = models.CharField(max_length=255)
    class Meta:
        db_table = 'club_zixun'

# 后台管理员表
class Myadmin(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=30)

    class Meta:
        db_table = 'myadmin'
