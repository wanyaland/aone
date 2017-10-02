"""
Custom django admin actions
"""


def refresh_save(modeladmin, request, queryset):
    """
    Does a save for all select queryset
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    for obj in queryset:
        obj.save()

refresh_save.short_description = "Refresh Save"