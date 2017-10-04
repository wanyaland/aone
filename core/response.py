"""
Some utility Response type
"""
from collections import namedtuple

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from core.codes import MAP
from core.constants import SUCCESS_OK
from core.config import COST_TYPE_DICT


class Response(object):
    """
    based on content type passed in , return appropriate response data
    """
    def __init__(self, request, data, template=None, content_type=None, status=200, api_status=SUCCESS_OK, **kwargs):
        self._request = request
        self.data = data
        self.content_type = content_type or request.META.get('CONTENT_TYPE', 'text/html')
        self.status = status
        self.api_status = api_status
        self.message = kwargs.get('message')
        self.template = template
        self.inject_categories = kwargs.get('inject_categories', True)
        self.response_type = kwargs.get('response_type')

    def __call__(self, *args, **kwargs):
        return self.write()

    def write(self):
        response_type = "html"
        if 'json' in self.content_type:
            response_type = "json"

        self.fuse_setting()
        self.fuse_api_code()
        return getattr(self, response_type+"_response")()

    def fuse_api_code(self):
        if isinstance(self.data, dict):
            api_status_code = self.data.get('code', self.api_status)
            # if (4000 <= api_status_code < 5000):
            #     status = 200
            if self.message is not None:
                self.data['message'] = self.message
            else:
                self.data['message'] = MAP[api_status_code]
            self.data['code'] = api_status_code

    def json_response(self):
        """
        A custom Json response util method
        :param data: python dictionary
        :param content_type: default content_type for json response
        :param status:
        :param formatter:
        :return: json response
        """
        content_type = 'application/json'
        self.data.pop('SETTINGS', None)
        if isinstance(self.data, dict) and 'data' in self.data and 'count' not in self.data:
            self.data['count'] = len(self.data['data'])
        return JsonResponse(self.data, content_type=content_type, status=self.status)

    def html_response(self):
        if isinstance(self.data, dict) and 'parent_categories' not in self.data and self.inject_categories:
            from app.common.views import CategoryView  # Avoid circular import
            self.data['parent_categories'] = CategoryView.get_data(parent=True)
        if self.template:
            if self.response_type == "ajax_html":
                html_render = loader.render_to_string(self.template, context=self.data, request=self._request)
                self.data['html'] = html_render
                return self.json_response()
            return render(self._request, self.template, self.data)
        return HttpResponse(self.data, status=self.status)

    def fuse_setting(self):
        setting_cons = ['GOOGLE_MAP_API_KEY']
        self.data['SETTINGS'] = {}
        for key in setting_cons:
            self.data['SETTINGS'][key] = getattr(settings, key)
        self.data['SETTINGS']['COST_TYPE'] = COST_TYPE_DICT

