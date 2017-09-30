from operator import and_, or_
from functools import reduce

from django.shortcuts import render
from django.db.models import Q
from django.views import View

from core.utils import update_dict

from app.business.models import Category
from core.config import BUSINESS
from core.response import Response


class CategoryView(View):
    """
    Return json data for Category
    """
    def get(self, request, *args, **kwargs):
        update_dict(kwargs, request.GET)
        category_id = kwargs.get('category_id')
        subcategory_id = kwargs.get('subcategory_id')
        response = {}
        data = self.get_data(category_id, subcategory_id)
        response['data'] = data
        return Response(request, response, content_type='json')()

    @staticmethod
    def get_data(category=None, subcategory=None):
        query = [Q(status=True) & Q(category_type=BUSINESS)]
        if subcategory is not None:
            query.append(Q(id=subcategory) & Q(parent_category__isnull=False))
            if category is not None:
                query.append(Q(parent_category__id=category))

        elif category is not None:
            query.append(Q(id=category))

        query_obj = reduce(and_, query)
        fields = ['id', 'name', 'parent_category']
        return list(Category.objects.filter(query_obj).values(*fields))