from django.contrib import admin

from core.admin import refresh_save, duplicate

from .models import City, Country, Category, FileUpload, Business, BusinessHour, \
    BusinessPhoto, Feature, Customer, Review, ReviewTag, Event, EventDiscussion, ListingFaq

admin.autodiscover()


@admin.register(ListingFaq)
class ListingFaqAdmin(admin.ModelAdmin):
    list_display = ['question']
    actions = [refresh_save, duplicate]
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'status']
    ordering = ['name', 'country']


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_category']
    ordering = ['name']
    actions = [refresh_save]
    pass


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'approved', 'popularity_rating', 'web_address', 'email', 'claimed']
    ordering = ['name']
    actions = [refresh_save, duplicate]
    filter_horizontal = ['categories', 'features']
    list_filter = ['exclusive', 'approved', 'claimed']
    pass


@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessPhoto)
class BusinessPhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', "status"]
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(EventDiscussion)
class EventDiscussionAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'business', 'rating']
    pass


@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'tag', 'ip_address', 'status', 'modify_date']
    list_filter = ['tag', 'status']
    pass







