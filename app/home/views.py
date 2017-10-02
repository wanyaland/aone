from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect

from core.response import Response
from core.mixin import PatchRequestKwargs

from .models import ContactUsRequest
from .forms import ContactUsForm


class HomeView(PatchRequestKwargs, View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return Response(request, {}, template=self.template_name, **kwargs)()


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

