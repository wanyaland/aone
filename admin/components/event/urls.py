from django.conf.urls import patterns, url
from admin.components.event import views

urlpatterns = [
    url(r'^list$', views.EventList.as_view(), name='event_list'),
    url(r'^create$', views.EventCreate.as_view(), name='event_create'),
    url(r'^update/(?P<pk>\d+)$', views.EventUpdate.as_view(), name='event_update'),
    url(r'^delete/(?P<pk>\d+)$', views.EventDelete.as_view(), name='event_delete'),
]