from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect

from core.response import Response
from core.mixin import PatchRequestKwargs

from app.common.views import CityView
from app.business.views import ListingView

from .models import ContactUsRequest
from .forms import ContactUsForm
from pprint import pprint


class HomeView(PatchRequestKwargs, View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        response = dict()
        response['cities'] = CityView.get_data()
        exclusive_listing = ListingView.get_data(exclusive=True)
        response['exclusive_listing'] = exclusive_listing.get('data', [])
        pprint(exclusive_listing)
        return Response(request, response, template=self.template_name, **kwargs)()


class AboutView(PatchRequestKwargs, View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return Response(request, {}, template=self.template_name, **kwargs)()


class ContactView(PatchRequestKwargs, View):
    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        return Response(request, {}, template=self.template_name, **kwargs)()

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/contact")

