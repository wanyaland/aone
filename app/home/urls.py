"""
Africaone home URL Configuration
"""
from django.conf.urls import url

from .views import HomeView, AboutView, ContactView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^index.html$', HomeView.as_view(), name='index'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact')
]