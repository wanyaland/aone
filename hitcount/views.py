import warnings
from collections import namedtuple

from django.http import Http404,JsonResponse,HttpResponseBadRequest
from django.conf import settings
from django.views.generic import View,DetailView
from django.shortcuts import render

from hitcount.utils import get_ip
from hitcount.models import Hit,HitCount

# Create your views here.

class HitCountMixin(object):
    @classmethod
    def hit_count(self,request,hitcount):
        UpdateHitCountResponse = namedtuple(
            'UpdateHitCountResponse','hit_counted hit_message'
        )
        if request.session.session_key is None:
            request.session.save()
        user = request.user
        session_key = request.session.session_key
        ip = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT','')[:255]
        qs = Hit.objects.filter_active()
        hit = Hit(session=session_key,hitcount=hitcount,ip=get_ip(request),
                  user_agent=request.META.get('HTTP_USER_AGENT','')[:255],)
        if user.is_authenticated():
            if not qs.filter(user=user,hitcount=hitcount):
                hit.user = user
                hit.save()

                response = UpdateHitCountResponse(
                    False,'Hit counted: user authentication'
                )
            else:
                response = UpdateHitCountResponse(
                    False,'Not counted:authenticated user has active hit'
                )
        else:
            if not qs.filter(session=session_key,hitcount=hitcount):
                hit.save()
                response = UpdateHitCountResponse(
                    True,'Hit counted:session key'
                )
            else:
                response = UpdateHitCountResponse(
                    False,'Not counted:session has active hit'
                )
        return response

class HitCountJSONView(View,HitCountMixin):
    '''
    JSON View to handle hit count post
    '''
    pass


