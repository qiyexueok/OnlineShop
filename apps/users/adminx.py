# -*- coding:utf-8 -*- 
__author__ = 'll'


import xadmin

from .models import UserProfile, VerifyCode
from xadmin import views


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True
    menu_style = 'accordin'


class GlobalSettings(object):
    site_title = '食品后台管理系统'
    site_footer = 'mx'


class UserProfileAdmin(object):
    pass


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)