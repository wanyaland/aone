from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns,url
from core.views import *
from djangoratings.views import AddRatingFromModel
from django.contrib.auth import login
from django.contrib.auth.views import *


urlpatterns = patterns (
    '',
    url(r'^$', index, name='home'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^login/', login_view, name='login'),
    url(r'^sign_up/', sign_up, name='sign_up'),
    url(r'^business/sign-up/', sign_up_business_view, name='sign_up_business'),
    url(r'^moderator/sign-up/',sign_up_moderator,name='sign_up_moderator'),
    url(r'^reset_password/',ResetPasswordRequestView.as_view(),name='reset_password'),
    url(r'^user/password/reset/$',password_reset,{'post_reset_redirect':'/user/password/reset/done/','template_name':'core/auth-user/forgot_password.html'},
        name='password_reset'),
    url(r'^user/password/reset/done/$',password_reset_done),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,
                                 {'post_reset_redirect':'/user/password/done'},name='reset_password_confirm'),
    url(r'^user/password/done/$',password_reset_complete  ),
    url(r'^business_list/$', BusinessList.as_view(), name='business_list'),
    url(r'^search_business/$', CategoryListingPageView.as_view(), name='search_business'),
    url(r'^find_business/$',find_business,name='search'),
    url(r'^business_add/$', BusinesView.as_view(), name='business_add'),
    url(r'^business_edit/(?P<pk>\d+)/$', BusinesView.as_view(), name='business_edit'),
    url(r'^add_business_successful', add_business_successful, name='add_business_successful'),
    url(r'^review_list', ReviewListView.as_view(), name='review_list'),
    url(r'^review_add/(?P<business_pk>\d+)/$', login_required(ReviewCreate.as_view()), name='review_add'),
    url(r'^review_edit/(?P<pk>\d+)/$', login_required(ReviewEdit.as_view()), name='review_edit'),
    url(r'^review_detail/(?P<pk>\d+)/$',ReviewDetail.as_view(),name='review_detail'),
    url(r'^business-user-edit/(?P<pk>\d+)/$', login_required(BusinessUserView.as_view()), name='business_user_edit'),
    url(r'business-user-add', login_required(BusinessUserView.as_view()), name='business_user_add'),
    url(r'business-detail/(?P<pk>\d+)/$', BusinessDetail.as_view(), name='business_detail'),
    #url(r'user-detail/(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'user-list', UserList.as_view(), name='user_list'),
    url(r'sign-up-business-results/$', ClaimBusinessList.as_view(), name='sign_up_business_results'),
    url(r'^get_home_page_businesses/$', GetHomePageBusinesses.as_view(), name='get_home_page_businesses'),
    url(r'^get_nearest_businesses/$', GetNearestBusinesses.as_view(), name='get_nearest_businesses'),
    url(r'^about-africaone/$', about, name='about_africaone'),
    url(r'^advertising/$', StaticAdvertisingView, name='advertising'),
    url(r'^privacy-policy/$', StaticPrivacyPolicyView, name='privacy_policy'),
    url(r'^terms-conditions/$', StaticTermsConditionsView, name='terms_conditions'),
    url(r'^add-business-success/$', AddBusinessSuccessView, name='add_business_success'),
    url(r'^category-name/(?P<pk>\d+)/$', CategoryLandingPageView.as_view(), name='category_name'),
    url(r'^category-name/listing/$', CategoryListingPageView.as_view(), name='category_name_listing'),
    url(r'^claim-business/find$', ClaimBusinessList.as_view(), name='claim_business_find'),
    url(r'^claim-business/(?P<pk>\d+)/$',claim_business,name='claim_business'),
    url(r'^user-detail/(?P<pk>\d+)/$', UserDetailTestPageView, name='user_detail_test'),
    url(r'^events/$', events_landing, name='events_landing'),
    url(r'^events/listing/$', events_listing, name='events_listing'),
    url(r'^event_detail/(?P<pk>\d+)/$', events_detail, name='events_full_view'),
    url(r'^events/create/$', create_event, name='events_create'),
    url(r'^event_comment/(?P<pk>\d+)/$',event_comment,name='event_comment'),
    url(r'^tag_review/$',tag_review,name='tag_review'),
    url(r'^upload_photo/(?P<pk>\d+)/$',upload_business_photos,name='upload_photos'),
    url(r'^mark_photo/(?P<pk>\d+)/$',mark_photo,name='mark_photo'),
    url(r'^news_list', NewsListView.as_view(), name='news_list'),
)

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)