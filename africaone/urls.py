"""
africaone URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from app.home.views import HomeView, AboutView, ContactView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^index.html$', HomeView.as_view(), name='home_index'),
    url(r'^about.html$', AboutView.as_view(), name='home_index'),
    url(r'^contact.html$', ContactView.as_view(), name='home_index'),
    url(r'^index.html$', HomeView.as_view(), name='home_index'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
