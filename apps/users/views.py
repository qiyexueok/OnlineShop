import string
import random

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import authentication
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from OnlineShop.settings import APIKEY

User = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = string.digits
        random_str = []
        for i in range(4):
            random_str.append(seeds[random.randint(0,9)])

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, mobile)
        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status['msg'],
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_recode = VerifyCode(code=code, mobile=mobile)
            code_recode.save()
            return Response({
                "moblie": mobile,
        }, status=status.HTPP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_class = (JSONWebTokenAuthentication,
                            authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()



















