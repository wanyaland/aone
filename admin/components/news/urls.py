from django.conf.urls import patterns, url
from admin.components.news import views

urlpatterns = [
    url(r'^list$', views.NewsList.as_view(), name='news_list'),
    url(r'^create$', views.NewsCreate.as_view(), name='news_create'),
    url(r'^update/(?P<pk>\d+)$', views.NewsUpdate.as_view(), name='news_update'),
    url(r'^delete/(?P<pk>\d+)$', views.NewsDelete.as_view(), name='news_delete'),
]