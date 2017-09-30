"""
AfricaOne Business URL Configuration
"""
from django.conf.urls import url

from .views import ListingView, DetailView

urlpatterns = [
    url(r'^', ListingView.as_view(), name='listing', kwargs={'sort': 'name'}),
    url(r'detail/(?P<slug>[-\w]+)/$', DetailView.as_view(), name="detail_slug"),
    url(r'detail/(?P<business_id>[-\d]+)/$', DetailView.as_view(), name="detail_id")

]