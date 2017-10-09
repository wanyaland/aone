from functools import reduce
from operator import or_, and_

from pprint import pprint

from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg, F, Count

from core.response import Response
from core.utils import update_dict, remove_dups_by_key, business_working_status, calculate_price_category
from core.mixin import PatchRequestKwargs

from app.business.models import Business, BusinessHour, Review
from app.common.views import CategoryView
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect


BUSINESS_LISTING_FIELDS = ['id', 'name', 'banner_photo', 'popularity_rating', 'slug', 'city__id',
                          'city__name', 'categories__id', 'categories__name', 'categories__icon',
                          'claimed', 'approved', 'web_address', 'phone_number', 'city', 'address', 'photo',
                          'longitude', 'latitude', 'email', 'start_time', 'end_time', 'description',
                          'price_min', 'price_max',
                          'business_hours__day', 'business_hours__opening_hours', 'business_hours__closing_hours']

COMBINE_KEYS = {'categories': ['categories__id', 'categories__name', 'categories__icon'],
                'business_hours': ['business_hours__day', 'business_hours__opening_hours',
                                   'business_hours__closing_hours']}


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
        response_type = kwargs.get('response_type')
        if response_type == "ajax_html":
            self.template_name = "listing/listing_body.html"
        sort_direction = kwargs.get('direction', 'asc') == 'desc' and '-' or ''
        count = kwargs.get('count', 10)
        if count > 100:
            count = 100
        page = kwargs.get('page', 1)
        category_id = int(kwargs.get('category_id') or 0)
        city_id = kwargs.get('city_id')

        inexpensive = kwargs.get('inexpensive')
        moderate = kwargs.get('moderate')
        pricey = kwargs.get('pricey')
        ultra = kwargs.get('ultra')
        cost_type = filter(None, [inexpensive, moderate, ultra, pricey])

        open_time = kwargs.get('open_time') == 'open'
        average_rate = kwargs.get('average_rate') == 'rating'
        most_reviewed = kwargs.get('most_reviewed') == 'reviewed'

        listing_data = self.get_data(sort_direction, sort_by, count, page,
                                     category_id=category_id,
                                     city_id=city_id,
                                     cost_type=cost_type,
                                     open_time=open_time,
                                     average_rate=average_rate,
                                     most_reviewed=most_reviewed)

        if category_id and len(listing_data['data']):
            kwargs['category_name'] = listing_data['data'][0]['categories__name'][0]
            kwargs['category_id'] = category_id

        listing_data['filters'] = kwargs
        response = Response(request, listing_data, template=self.template_name, **kwargs)()
        return response

    @staticmethod
    def get_data(sort_direction='-', sort_by='name', count=10, page=1, category_id=None, city_id=None,
                 exclusive=False, cost_type=None, open_time=False, average_rate=False, most_reviewed=False):
        select_extra = {}

        cost_type = cost_type or []
        child_categories = []
        query_obj = Q(status=True)
        if category_id:
            query_obj &= Q(categories__id=category_id)
            child_categories = CategoryView.get_data(parent_category=category_id)
        if city_id:
            query_obj &= Q(city__id=city_id)

        if exclusive:
            query_obj &= Q(exclusive=True)

        business_listing = list(Business.objects.filter(query_obj)
                                .extra(select=select_extra)
                                .order_by(sort_direction+sort_by)
                                .values(*BUSINESS_LISTING_FIELDS))

        unique_listing_, unique_listing_id = remove_dups_by_key(business_listing, by_key=COMBINE_KEYS['categories']+COMBINE_KEYS['business_hours'])

        ## get average rating
        averaged_review_ = list(Review.objects.filter(business__id__in=[1, 2], status=True).values("business__id").annotate(
            avg_rating=Sum('rating') / Count('rating'), count=Count('rating')))

        averaged_review = {review['business__id']: [review['avg_rating'], review['count']] for review in averaged_review_}

        result_set = []
        for row in unique_listing_:
            for key, values in COMBINE_KEYS.items():
                val = list(map(lambda ck: row[ck], values))
                row[key] = zip(*val)

            row['business_hours_show'] = business_working_status(row['business_hours'])
            row['cost_type'] = calculate_price_category(row['price_min'], row['price_max'])
            row['avg_rating'] = averaged_review.get(row['id'], [0, 0])[0]
            row['review_count'] = averaged_review.get(row['id'], [0, 0])[1]

            include_in_final_result = True

            if open_time and row['business_hours_show']['status']!=True:
                include_in_final_result = False
            if cost_type and include_in_final_result and row['cost_type']['form_id'] not in cost_type:
                include_in_final_result = False

            if include_in_final_result:
                result_set.append(row)

        sort_key = (most_reviewed and 'review_count') or (average_rate and 'avg_rating') or None

        if sort_key:
            result_set = sorted(result_set, key=lambda row: row[sort_key], reverse=True)

        pages = Paginator(result_set, count)
        response = {'count': pages.count, 'data': [], 'total_pages': pages.num_pages, 'child_categories': child_categories}

        if pages.num_pages <= page:
            objects_list = pages.page(page).object_list
            response['data'] = objects_list
            response['show_header_search'] = True
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
        business_listing_ = list(Business.objects.filter(query_obj)
                                .extra(select=select_extra)
                                .values(*BUSINESS_LISTING_FIELDS))
        if len(business_listing_):
            business_listing, unique_listing_id = remove_dups_by_key(business_listing_, by_key=COMBINE_KEYS['categories']+COMBINE_KEYS['business_hours'])
            for obj in business_listing:
                for key, values in COMBINE_KEYS.items():
                    val = list(map(lambda ck: obj[ck], values))
                    obj[key] = zip(*val)

            response['data'] = business_listing[0]
            response['data']['business_hours_show'] = business_working_status(response['data']['business_hours'])
            response['data']['cost_type'] = calculate_price_category(response['data']['price_min'], response['data']['price_max'])
        return response


class SearchView(View):
    """
    search view
    Accepts only one query parameter named query
    """
    def get(self, request, *args, **kwargs):
        data = {}
        return Response(request, data, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(username=username,password=password)
          login(request,user)
          return redirect('home')
        else:
          form = UserCreationForm()
    return render(request,'signup.html',{'form':form})
