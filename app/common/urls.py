"""
AfricaOne Business URL Configuration
"""
from django.conf.urls import url

from .views import CategoryView, ContactRequestView

urlpatterns = [
    url(r'category/$', CategoryView.as_view(), name='category'),
    url(r'category/parent/$', CategoryView.as_view(), name="category_parent", kwargs={'parent': True}),
    url(r'category/(?P<category_id>[-\d]+)/$', CategoryView.as_view(), name="category_id"),
    url(r'category/(?P<category_id>[-\d]+)/(?P<subcategory_id>[-\d]+)/$', CategoryView.as_view(), name="category_parent_sub"),
    url(r'category/all/(?P<subcategory_id>[-\d]+)/$', CategoryView.as_view(), name="category_sub"),

    url(r'category/search/$', CategoryView.as_view(), name="category_search"),
    url(r'category/search/(?P<category_name>[-\w]+)/$', CategoryView.as_view(), name="category_search_kwargs"),

    url(r'contact/request/$', ContactRequestView.as_view(), name="contact_request"),

]