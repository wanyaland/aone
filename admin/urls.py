from django.conf.urls import patterns,url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns(
    '',
    url(r'^login/$',views.login_user,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^$',views.BusinessList.as_view(),name='home'),
    url(r'^create_business/$',views.BusinessCreate.as_view(),name='create_business'),
    url(r'^get_categories/$',views.categories_json,name='get_categories'),
    url(r'^manage_business_photos/(?P<pk>\d+)/$',views.manage_business_photos,name='manage_business_photos'),
    url(r'^manage_categories/$',views.ManageCategories.as_view(),name='manage_categories'),
    url(r'^delete_business/(?P<pk>\d+)/$',views.BusinessDelete.as_view(),name='delete_business'),
    url(r'^update_business/(?P<pk>\d+)/$',views.BusinessUpdate.as_view(),name='update_business'),
    url(r'^create_parent_category/$',views.ParentCategoryCreate.as_view(),name='create_parent_category'),
    url(r'^update_parent_category/$',views.ParentCategoryUpdate.as_view(), name='update_parent_category'),
    url(r'^delete_parent_category/$',views.delete_parent_category, name='delete_parent_category'),
    url(r'^create_sub_category/$',views.CategoryCreate.as_view(),name='create_sub_category'),
    url(r'^edit_sub_category/$',views.CategoryUpdate.as_view(),name='edit_sub_category'),
    url(r'^delete_sub_category/$',views.delete_category,name='delete_sub_category'),
    url(r'^upload_business_photos/$',views.UploadBusinessPhotos.as_view(),
        name='upload_business_photos'),
    url(r'^upload_banner_image/$',views.UploadBannerImage.as_view(),
        name='upload_banner'),
    url(r'^upload_business_logo/$',views.UploadLogo.as_view(),
        name='upload_business_logo'),
    url(r'^delete_business_photo/$',views.DeleteBusinessImage.as_view(),
        name='delete_business_image'),
    url(r'^edit_business_caption/$',views.EditCaption.as_view(),
        name='edit_business_caption'),
    url(r'^delete_business_banner/$',views.DeleteBannerImage.as_view(),
        name='delete_business_banner'),
    url(r'^delete_business_logo/$',views.DeleteLogoImage.as_view(),
        name='delete_business_logo'),
    url(r'^get_all_categories/$',views.GetCategories.as_view(),
        name='get_all_categories'),
    url(r'^manage-reviews/$',views.ManageReviews.as_view(),
        name='manage_reviews'),
    url(r'^manage-users/$',views.ManageUsers.as_view(),
        name='manage_users'),
    url(r'^create-users/$',views.CreateUser.as_view(),
        name='create_user'),
    url(r'^news/list$', views.NewsList.as_view(), name='news_list'),
    url(r'^news/create$', views.NewsCreate.as_view(), name='news_create'),
    url(r'^news/update/(?P<pk>\d+)$', views.NewsUpdate.as_view(), name='news_update'),
    url(r'^news/delete/(?P<pk>\d+)$', views.NewsDelete.as_view(), name='news_delete'),
    url(r'^news_category/list$', views.NewsCategoryList.as_view(), name='news_category_list'),
    url(r'^news_category/create$', views.NewsCategoryCreate.as_view(), name='news_category_create'),
    url(r'^news_category/update/(?P<pk>\d+)$', views.NewsCategoryUpdate.as_view(), name='news_category_update'),
    url(r'^news_category/delete/(?P<pk>\d+)$', views.NewsCategoryDelete.as_view(), name='news_category_delete'),
    url(r'^event_category/list$', views.EventCategoryList.as_view(), name='event_category_list'),
    url(r'^event_category/create$', views.EventCategoryCreate.as_view(), name='event_category_create'),
    url(r'^event_category/update/(?P<pk>\d+)$', views.EventCategoryUpdate.as_view(), name='event_category_update'),
    url(r'^event_category/delete/(?P<pk>\d+)$', views.EventCategoryDelete.as_view(), name='event_category_delete'),
)