"""
AfricaOne Master URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.home.urls')),
    url(r'^business/', include('app.business.urls')),
    url(r'^common/', include('app.common.urls')),
    url(r'^blog/$', TemplateView.as_view(template_name="message.html"), name="blog", kwargs={'message': 'Under Construction! '}),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


