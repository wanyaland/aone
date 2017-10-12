from django.contrib import admin

from core.admin import refresh_save, duplicate

from .models import ContactRequest, EmailOutbox

admin.autodiscover()


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'review_status', 'create_date', 'modify_date']
    list_filter = ['review_status']


@admin.register(EmailOutbox)
class EmailOutboxAdmin(admin.ModelAdmin):
    list_display = ['email_to', 'email_from', 'email_subject', 'status']
    pass


