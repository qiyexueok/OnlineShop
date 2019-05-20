from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name = '商品', help_text='商品ID')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'goods']

    def __str__(self):
        return self.user.username


class UserLeavingMessage(models.Model):
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    message_type = models.IntegerField(default='', choices=MESSAGE_CHOICES, verbose_name='留言类型', help_text='留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)')
    subject = models.CharField(default='', max_length=100, verbose_name='主题')
    message = models.TextField(default='', verbose_name='留言', help_text='留言内容')
    file = models.FileField(upload_to='message/images/', verbose_name='上传文件', help_text='上传文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    province = models.CharField(default='', max_length=100, verbose_name='省份')
    city = models.CharField(default='', max_length=100, verbose_name='城市')
    district = models.CharField(default='', max_length=100, verbose_name='区域')
    address = models.CharField(default='', max_length=200, verbose_name='详细地址')
    signer_name = models.CharField(default='', max_length=100, verbose_name='签收人')
    signer_mobile = models.CharField(default='', max_length=11, verbose_name='签收人电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

