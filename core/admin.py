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
        obj.save(refresh=True)

refresh_save.short_description = "Refresh Save"


def duplicate(modeadmin, request, queryset):
    """
    Duplicate the selected result set
    :param modeadmin:
    :param request:
    :param queryset:
    :return:
    """
    for obj in queryset:
        obj.id = None
        if hasattr(obj, 'name'):
            obj.name = obj.name+"_(duplicate)"
        elif hasattr(obj, 'title'):
            obj.title = obj.title+"_(duplicate)"
        obj.save()