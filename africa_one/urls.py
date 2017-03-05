from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'africa_one.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'',include('social.apps.django_app.urls',namespace='social')),
    url(r'^',include('core.urls',namespace='core')),
    url(r'^activity/',include('actstream.urls')),
    url(r'^manager/',include('admin.urls',namespace='admin')),
)