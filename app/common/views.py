from operator import and_, or_
from functools import reduce

from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.core.urlresolvers import reverse

from core.utils import update_dict

from app.business.models import Category, City
from core.config import BUSINESS
from core.response import Response
from core.mixin import PatchRequestKwargs

from .forms import ContactRequestForm

class CategoryView(PatchRequestKwargs, View):
    """
    Return json data for Category
    """
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        subcategory_id = kwargs.get('subcategory_id')
        category_name = kwargs.get('category_name')
        parent_only = kwargs.get('parent', False)
        response = {}
        data = self.get_data(category_id, subcategory_id, category_name, parent=parent_only)
        response['data'] = data
        return Response(request, response, content_type='json')()

    @staticmethod
    def get_data(category=None, subcategory=None, category_name=None, parent=False, parent_category=None):
        query = [Q(status=True) & Q(category_type=BUSINESS)]
        if subcategory is not None:
            query.append(Q(id=subcategory) & Q(parent_category__isnull=False))
            if category is not None:
                query.append(Q(parent_category__id=category))

        elif category is not None:
            query.append(Q(id=category))
        elif category_name is not None:
            query.append(Q(name__icontains=category_name))
        elif parent:
            query.append(Q(parent_category__isnull=True))

        if parent_category:
            query.append(Q(parent_category__id=parent_category))

        query_obj = reduce(and_, query)
        fields = ['id', 'name', 'parent_category', 'slug']
        return list(Category.objects.filter(query_obj).values(*fields))


class CityView(PatchRequestKwargs, View):
    def get(self, request, *args, **kwargs):
        city = kwargs.get('city')
        data = self.get_data(city)
        return Response(request, data, content_type='json')

    @staticmethod
    def get_data(city=None):
        query = Q(status=True)
        if city:
            query &= Q(id=city)

        return list(City.objects.filter().values('id', 'name', 'country__id', 'country__name'))


class ContactRequestView(View):

    def post(self, request, *args, **kwargs):
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact')+"?contact=1")
        else:
            msg = str(form.errors)
            return render(request, 'message.html', context={'message': msg})
