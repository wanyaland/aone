"""
Some global mixinx
"""

from core.utils import update_dict


class PatchRequestKwargs(object):
    def dispatch(self, request, *args, **kwargs):
        update_dict(kwargs, request.GET)
        return super(PatchRequestKwargs, self).dispatch(request, *args, **kwargs)