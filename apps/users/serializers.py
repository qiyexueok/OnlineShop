# -*- coding:utf-8 -*- 
__author__ = 'll'


import re
from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import VerifyCode
from OnlineShop.settings import REGEX_MOBILE

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        if re.match(REGEX_MOBLIE, mobile):
            raise serializers.ValidationError("手机号码非法")
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送时间未超过１分钟")

        return mobile



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码', error_messages={
        "blank": "请输入验证码",
        "required": "请输入验证码",
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误",
    }, help_text='验证码')
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(style={'input_type':'password'},
        help_text='密码', label ='密码', write_only=True)

    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_code:
            last_record = verify_code[0]
            five_minutes = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes > last_record.add_time:
                raise serializers.ValidationError('验证码已经过期')
            if last_record != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

        def validate(self, attrs):
            attrs['mobile'] = attrs['username']
            del attrs['code']
            return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'password', 'mobile')






