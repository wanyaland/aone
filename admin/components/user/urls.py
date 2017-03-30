from django.conf.urls import patterns, url
from admin.components.user import views

urlpatterns = [
    url(r'^list$', views.UserList.as_view(), name='user_list'),
    url(r'^create$', views.UserCreate.as_view(), name='user_create'),
    url(r'^update/(?P<pk>\d+)$', views.UserUpdate.as_view(), name='user_update'),
    url(r'^delete/(?P<pk>\d+)$', views.UserDelete.as_view(), name='user_delete'),
]