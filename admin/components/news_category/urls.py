from django.conf.urls import patterns, url
from admin.components.news_category import views

urlpatterns = [
    url(r'^list$', views.NewsCategoryList.as_view(), name='news_category_list'),
    url(r'^create$', views.NewsCategoryCreate.as_view(), name='news_category_create'),
    url(r'^update/(?P<pk>\d+)$', views.NewsCategoryUpdate.as_view(), name='news_category_update'),
    url(r'^delete/(?P<pk>\d+)$', views.NewsCategoryDelete.as_view(), name='news_category_delete'),
]