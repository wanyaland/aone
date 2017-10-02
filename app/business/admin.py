from django.contrib import admin

from core.admin import refresh_save

from .models import Country, Category, FileUpload, Business, BusinessHour, \
    BusinessPhoto, Feature, Customer, Review, ReviewTag, Event, EventDiscussion

admin.autodiscover()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


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
    actions = [refresh_save]
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
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(EventDiscussion)
class EventDiscussionAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    pass







