from django.conf.urls import patterns,url
from core.views import *
from djangoratings.views import AddRatingFromModel
from django.contrib.auth import login


urlpatterns = patterns (
    '',
    url(r'^$', index, name='home'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^login/', login_view, name='login'),
    url(r'^sign_up/', sign_up, name='sign_up'),
    url(r'^business/sign-up/', sign_up_business_view, name='sign_up_business'),
    url(r'^forgot-password/', forgot_password_view, name='forgot_password'),
    url(r'^business_list/$', BusinessList.as_view(), name='business_list'),
    url(r'^search_business/$', search_business, name='search_business'),
    url(r'^business_add', BusinesView.as_view(), name='business_add'),
    url(r'^business_edit/(?P<pk>\d+)/$', BusinesView.as_view(), name='business_edit'),
    url(r'^add_business_successful', add_business_successful, name='add_business_successful'),
    url(r'^review_list', ReviewListView.as_view(), name='review_list'),
    url(r'^review_add/(?P<business_pk>\d+)/$', ReviewCreate.as_view(), name='review_add'),
    url(r'^review_edit/(?P<pk>\d+)/$', ReviewEdit.as_view(), name='review_edit'),
    url(r'^business-user-edit/(?P<pk>\d+)/$', BusinessUserView.as_view(), name='business_user_edit'),
    url(r'business-user-add', BusinessUserView.as_view(), name='business_user_add'),
    url(r'business-detail/(?P<pk>\d+)/$', BusinessDetail.as_view(), name='business_detail'),
    url(r'user-detail/(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'user-list', UserList.as_view(), name='user_list'),
    url(r'sign-up-business-results/$', ClaimBusinessList.as_view(), name='sign_up_business_results'),
    url(r'^get_home_page_businesses/$', GetHomePageBusinesses.as_view(), name='get_home_page_businesses'),
    url(r'^get_nearest_businesses/$', GetNearestBusinesses.as_view(), name='get_nearest_businesses'),
    url(r'^about-africaone/$', about, name='about_africaone'),
    url(r'^advertising/$', StaticAdvertisingView, name='advertising'),
    url(r'^privacy-policy/$', StaticPrivacyPolicyView, name='privacy_policy'),
    url(r'^terms-conditions/$', StaticTermsConditionsView, name='terms_conditions'),
    url(r'^add-business-success/$', AddBusinessSuccessView, name='add_business_success'),
    url(r'^category-name/$', CategoryLandingPageView, name='category_name'),
    url(r'^category-name/listing/$', CategoryListingPageView, name='category_name_listing'),
    url(r'^claim-business/find$', claim_business_find_page, name='claim_business_find'),
    url(r'^user-detail-test$', UserDetailTestPageView, name='user_detail_test'),
    url(r'^events$', events_landing, name='events_landing'),
    url(r'^events/listing$', events_listing, name='events_listing'),
    url(r'^events/event-name$', EventsFullPageView, name='events_full_view'),
    url(r'^events/create$', create_event, name='events_create'),
)
