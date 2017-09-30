"""
AfricaOne Business URL Configuration
"""
from django.conf.urls import url

from .views import CategoryView

urlpatterns = [
    url(r'category/$', CategoryView.as_view(), name='category'),
    url(r'category/(?P<category_id>[-\d]+)/$', CategoryView.as_view(), name="category_id"),
    url(r'category/(?P<category_id>[-\d]+)/(?P<subcategory_id>[-\d]+)/$', CategoryView.as_view(), name="category_parent_sub"),
    url(r'category/all/(?P<subcategory_id>[-\d]+)/$', CategoryView.as_view(), name="category_sub")

]