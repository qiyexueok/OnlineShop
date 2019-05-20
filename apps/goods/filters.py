# -*- coding:utf-8 -*- 
__author__ = 'll'


import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(field_name='shop_price', help_text='最低价格', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', help_text='最高价格', lookup_expr='lte')
    top_catetory = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parnet_category_id=value))

    class Meta():
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']


# class GoodsFilter(django_filters.rest_framework.FilterSet):
#     """
#     商品的过滤类
#     """
#     pricemin = django_filters.NumberFilter(name='shop_price', help_text="最低价格",lookup_expr='gte')
#     pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
#     top_category = django_filters.NumberFilter(method='top_category_filter')
#
#
#     def top_category_filter(self, queryset, name, value):
#         return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
#
#
#     class Meta:
#         model = Goods
#         fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
