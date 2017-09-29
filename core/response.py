"""
Some utility Response type
"""
from django.http import HttpResponse, JsonResponse
from core.codes import MAP
from core.constants import SUCCESS_OK


class Response(object):
    """
    based on content type passed in , return appropriate response data
    """
    def __init__(self, data, content_type="application/json", status=200, api_status=SUCCESS_OK, **kwargs):
        self.data = data
        self.content_type = content_type
        self.status = status
        self.api_status = api_status
        self.message = kwargs.get('message')

    def write(self):
        response_type = "html"
        if 'json' in self.content_type:
            response_type = "json"

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
        return JsonResponse(self.data, content_type=content_type, status=self.status)

    def html_response(self):
        return HttpResponse(self.data, status=self.status)