"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
import rest_framework
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, GoodsCategoryViewSet, HotSearchViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import UserViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet
from user_operation.views import AddressViewSet, LeavingMessageViewSet, UserFavViewSet
from .settings import MEDIA_ROOT


router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'goodscategory', GoodsCategoryViewSet, base_name='goodscategory')
router.register(r'hotsearch', HotSearchViewSet, base_name='hotsearch')
router.register(r'banner', BannerViewSet, base_name='banner')
router.register(r'indexgoods', IndexCategoryViewSet, base_name='indexgoods')

router.register(r'user', UserViewSet, base_name='user')

router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'messages', LeavingMessageViewSet, base_name='messages')
router.register(r'address', AddressViewSet, base_name='address')

router.register(r'messages', LeavingMessageViewSet, base_name='messages')
router.register(r'address', AddressViewSet, base_name='address')

router.register(r'shopcart', ShoppingCartViewSet, base_name="shopcarts")
router.register(r'orders', OrderViewSet, base_name="orders")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^login/$', obtain_jwt_token),
]
