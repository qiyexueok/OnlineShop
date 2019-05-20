# -*- coding:utf-8 -*- 
__author__ = 'll'


import xadmin

from .models import Goods, GoodsCategory, GoodsCategoryBrand, IndexAd, GoodsImage, Banner, HotSearchWords


class GoodsAdmin(object):
    list_display = ['name', 'category', 'goods_front_image', 'click_num']
    style_fields={'goods_desc': 'ueditor'}
    search_fields = ['name', 'goods_brief']
    list_editable = ['is_hot',]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",  "shop_price", "is_new", "is_hot"]

    class GoodsImageInline(object):
        model = GoodsImage
        exclude = ['add_time']
        extra = 1
        style = 'tab'

    inlines = [GoodsImageInline]

class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodsImageAdmin(object):
    list_display = ["goods", "image"]
    list_filter = ["goods" ]
    search_fields = ['goods' ]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


class GoodsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]

    def get_context(self):
        context = super(GoodsBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
            return context

class BannerAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchWordsAdmin(object):
    list_display = ["keywords", "index", "add_time"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)

