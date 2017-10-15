"""
AfricaOne Business URL Configuration
"""
from django.conf.urls import url,include

from .views import ListingView, DetailView, SearchView, \
    ListingReview, signup, ReviewTagView, BusinessBookmarkView,account_activation_sent,activate


from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', ListingView.as_view(), name='listing', kwargs={'sort': 'name'}),
    url(r'listing/$', ListingView.as_view(), name='listing_all', kwargs={'sort': 'name'}),
    url(r'listing/review/$', ListingReview.as_view(), name='review_url'),
    url(r'listing/review/tag/$', ReviewTagView.as_view(), name='review_tag'),
    url(r'listing/(?P<category_id>[-\d]+)/$', ListingView.as_view(), name="listing_category"),
    url(r'listing/(?P<category_name>[-\w]+)/(?P<category_id>[-\d]+)/$', ListingView.as_view(), name='listing_slug_id', kwargs={'sort': 'name'}),
    url(r'detail/(?P<business_id>[-\d]+)/$', DetailView.as_view(), name="detail_id"),
    url(r'detail/(?P<slug>[-\w]+)/$', DetailView.as_view(), name="detail_slug"),
    url(r'location/listing/$', ListingView.as_view(), name='home_search_listing_all'),
    url(r'location/(?P<city_id>[-\d]+)/$', ListingView.as_view(), name='home_search_listing_city'),
    url(r'location/(?P<category_id>[-\d]+)/(?P<city_id>[-\d]+)/$', ListingView.as_view(), name='home_search_listing'),
    url(r'feature/(?P<feature_id>[-\d]+)/$', ListingView.as_view(), name="listing_feature"),
    url(r'signup/$',signup,name='signup'),
    url(r'login/$',auth_views.login,name='login'),
    url(r'logout/$',auth_views.logout,name='logout'),
    url(r'oauth/',include('social_django.urls',namespace='social')),
    url(r'search/$', SearchView.as_view(), name='search'),
    url(r'^account_activation_sent/$',account_activation_sent,name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate,name='activate'),

    url(r'bookmark/$', BusinessBookmarkView.as_view(), name='bookmark'),


    # business admin, fake or not valid view
    url(r'user/admin/(?P<user_id>[-\d]+)/$', SearchView.as_view(), name='business_admin_dashboard'),
    url(r'user/admin/profile/(?P<user_id>[-\d]+)/$', SearchView.as_view(), name='business_admin_profile'),

]
