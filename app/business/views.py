from functools import reduce
from operator import or_, and_

from pprint import pprint

from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q

from core.response import Response
from core.utils import update_dict, remove_dups_by_key
from core.mixin import PatchRequestKwargs

from app.business.models import Business, BusinessHour
from app.common.views import CategoryView


class ListingView(PatchRequestKwargs, View):
    """
    This takes several parameters and then return the appropriate response to frontend
    """
    template_name = "listing/listing.html"

    def get(self, request, *args, **kwargs):
        """
        Accepts some
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        sort_by = kwargs.get('sort', 'name')
        sort_direction = kwargs.get('direction', 'asc') == 'desc' and '-' or ''
        count = kwargs.get('count', 10)
        if count > 100:
            count = 100
        page = kwargs.get('page', 1)
        category_id = kwargs.get('category_id')
        listing_data = self.get_data(sort_direction, sort_by, count, page, category_id=category_id)

        listing_data['filters'] = kwargs
        # pprint(listing_data)
        response = Response(request, listing_data, template=self.template_name, **kwargs)()
        return response

    @staticmethod
    def get_data(sort_direction, sort_by, count, page, category_id=None):
        select_extra = {}
        fields = ['id', 'name', 'slug', 'country', 'categories__id', 'categories__name', 'categories__icon']
        query_obj = Q(status=True)
        if category_id:
            query_obj &= Q(categories__id=category_id)

        business_listing = list(Business.objects.filter(query_obj)
                                .extra(select=select_extra)
                                .order_by(sort_direction+sort_by)
                                .values(*fields))

        combine_keys = {'categories': ['categories__id', 'categories__name', 'categories__icon']}
        uniqure_listing_ = remove_dups_by_key(business_listing, by_key=combine_keys['categories'])

        pages = Paginator(uniqure_listing_, count)
        response = {'count': pages.count, 'data': [], 'total_pages': pages.num_pages}
        if pages.num_pages <= page:
            objects_list = pages.page(page).object_list
            for obj in objects_list:
                for key, values in combine_keys.items():
                    val = list(map(lambda ck: obj[ck], values))
                    obj[key] = zip(*val)
            response['data'] = objects_list
        return response


class DetailView(PatchRequestKwargs, View):
    """
    Business listing detail view
    """
    template_name = "listing/detail.html"

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        business_id = kwargs.get('business_id')
        business_listing = self.get_data(slug, business_id)
        return Response(request, business_listing, template=self.template_name, **kwargs)()

    @staticmethod
    def get_data(slug=None, business_id=None):
        response = {}

        if not (slug or business_id):
            return response

        query_slug_id = reduce(or_, [Q(slug=slug),  Q(id=business_id)])
        query_obj = reduce(and_, [query_slug_id, Q(status=True)])
        select_extra = {}
        fields = ['id', 'name', 'banner_photo', 'popularity_rating', 'slug', 'country', 'categories__id', 'categories__name', 'categories__icon', 'claimed',
                  'approved', 'web_address', 'phone_number', 'city', 'address', 'photo', 'longitude', 'latitude',
                  'email', 'start_time', 'end_time', 'description', 'price_min', 'price_max',
                  'business_hours__day', 'business_hours__opening_hours', 'business_hours__closing_hours']

        business_listing_ = list(Business.objects.filter(query_obj)
                                .extra(select=select_extra)
                                .values(*fields))
        combine_keys = {'categories': ['categories__id', 'categories__name', 'categories__icon'], 'business_hours': ['business_hours__day', 'business_hours__opening_hours', 'business_hours__closing_hours']}
        if len(business_listing_):
            business_listing = remove_dups_by_key(business_listing_, by_key=combine_keys['categories']+combine_keys['business_hours'])
            for obj in business_listing:
                for key, values in combine_keys.items():
                    pprint(zip(*map(lambda ck: obj[ck], values)))
                    obj[key] = zip(*map(lambda ck: obj[ck], values))

            response['data'] = business_listing[0]
        return response
