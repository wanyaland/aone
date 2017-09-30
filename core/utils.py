import datetime
import time

from django.utils.text import slugify


def get_slug(value, unique=True, allow_unicode=False):
    value = slugify(value, allow_unicode)
    if unique:
        time_stamp = str(int(round(time.time() * 1000)))
        value += "_"+time_stamp
    return value


def update_dict(dict1, dict2):
    """
    TODO: use dict.update
    Can not use dict.update due to behavior of request.GET and request.POST
    :param dict1:
    :param dict2:
    :return: return dict1
    """
    if type(dict1) is type(dict2) and isinstance(dict1, dict):
        for key in dict2:
            dict1[key] = dict2[key]
        return dict1
    return None
