"""
All related to listing
"""
from django.views import View
from django.shortcuts import render, redirect

from core.response import Response

from app.common.models import Business


class ListingView(View):
    template_name = "listing.html"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def get_data(self, **kwargs):
        """
        return plain python dict to represent product data
        this can later be used in django template or as json response type
        :return:
        """

class DetailView(View):
    """
    Return Product Data by product Id
    :param View:
    :return:
    """
    template_name = "detail.html"

    def get(self, request, *args, **kwargs):
        pass

    def get_data(self, **kwrags):
        """
        return plain python dictionary representing the product data
        :param kwrags:
        :return:
        """