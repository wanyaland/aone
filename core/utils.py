import datetime
import time

from django.utils.text import slugify


def get_slug(value, unique=True, allow_unicode=False):
    value = slugify(value, allow_unicode)
    if unique:
        time_stamp = str(int(round(time.time() * 1000)))
        value += "_"+time_stamp
    return value