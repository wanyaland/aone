from functools import reduce
from operator import or_, and_

from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q

from core.response import Response
from core.utils import update_dict

from app.business.models import Business


class ListingView(View):
    """
    This takes several parameters and then return the appropriate response to frontend
    """
    template_name = "listing.html"

    def get(self, request, *args, **kwargs):
        """
        Accepts some
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        update_dict(kwargs, request.GET)
        sort_by = kwargs.get('sort', 'name')
        sort_direction = kwargs.get('direction', 'asc') == 'desc' and '-' or ''
        count = kwargs.get('count', 10)
        if count > 100:
            count = 100
        page = kwargs.get('page', 1)
        category_id = kwargs.get('category_id')
        listing_data = self.get_data(sort_direction, sort_by, count, page, category_id=category_id)
        response = Response(request, listing_data, template=self.template_name, **kwargs)()
        return response

    @staticmethod
    def get_data(sort_direction, sort_by, count, page, category_id=None):
        select_extra = {}
        fields = ['id', 'name', 'slug', 'country', 'categories']
        query_obj = Q(status=True)
        if category_id:
            query_obj &= Q(categories__id=category_id)

        business_listing = list(Business.objects.filter(query_obj)\
            .extra(select=select_extra)\
            .order_by(sort_direction+sort_by)\
            .values(*fields))
        pages = Paginator(business_listing, count)
        response = {'count': pages.count, 'data': [], 'total_pages': pages.num_pages}
        if pages.num_pages <= page:
            response['data'] = pages.page(page).object_list
        return response


class DetailView(View):
    """
    Business listing detail view
    """
    template_name = "detail.html"

    def get(self, request, *args, **kwargs):
        update_dict(kwargs, request.GET)
        slug = kwargs.get('slug')
        business_id = kwargs.get('business_id')
        business_listing = self.get_data(slug, business_id)
        return Response(request, business_listing, template=self.template_name)

    @staticmethod
    def get_data(slug=None, business_id=None):
        response = {}

        if not (slug or business_id):
            return response

        query_slug_id = reduce(or_, [Q(slug=slug),  Q(id=id)])
        query_obj = reduce(and_, [query_slug_id, Q(status=True)])
        select_extra = {}
        fields = ['id', 'name', 'slug', 'country', 'categories']

        business_listing = list(Business.objects.filter(query_obj)\
            .extra(select=select_extra)\
            .values_list(*fields))
        if len(business_listing):
            response['data'] = business_listing[0]
        return response
