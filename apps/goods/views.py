from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, GoodsCategoryBrand, IndexAd, GoodsImage, Banner, HotSearchWords
from .serializers import GoodsSerializer, GoodsCategorySerializer, HotSearchSerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class HotSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class = HotSearchSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['水果'])
    serializer_class = IndexCategorySerializer


