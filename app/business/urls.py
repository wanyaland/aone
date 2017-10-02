"""
AfricaOne Business URL Configuration
"""
from django.conf.urls import url

from .views import ListingView, DetailView

urlpatterns = [
    url(r'^$', ListingView.as_view(), name='listing', kwargs={'sort': 'name'}),
    url(r'listing/$', ListingView.as_view(), name='listing_all', kwargs={'sort': 'name'}),
    url(r'listing/(?P<category_id>[-\d]+)/$', ListingView.as_view(), name="listing_category"),
    url(r'listing/(?P<category_name>[-\w]+)/(?P<category_id>[-\d]+)/$', ListingView.as_view(), name='listing_slug_id', kwargs={'sort': 'name'}),
    url(r'detail/(?P<slug>[-\w]+)/$', DetailView.as_view(), name="detail_slug"),
    url(r'detail/(?P<business_id>[-\d]+)/$', DetailView.as_view(), name="detail_id"),
    url(r'location/listing/$', ListingView.as_view(), name='home_search_listing_all'),
    url(r'location/(?P<city_id>[-\d]+)/$', ListingView.as_view(), name='home_search_listing_city'),
    url(r'location/(?P<category_id>[-\d]+)/(?P<city_id>[-\d]+)/$', ListingView.as_view(), name='home_search_listing')
]