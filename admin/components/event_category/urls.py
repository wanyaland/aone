from django.conf.urls import patterns, url
from admin.components.event_category import views

urlpatterns = [
    url(r'^list$', views.EventCategoryList.as_view(), name='event_category_list'),
    url(r'^create$', views.EventCategoryCreate.as_view(), name='event_category_create'),
    url(r'^update/(?P<pk>\d+)$', views.EventCategoryUpdate.as_view(), name='event_category_update'),
    url(r'^delete/(?P<pk>\d+)$', views.EventCategoryDelete.as_view(), name='event_category_delete'),
]