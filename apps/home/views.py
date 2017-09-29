from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect

from .models import ContactUsRequest
from .forms import ContactUsForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class AboutView(View):
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class ContactView(View):
    template_name = "contactus_old.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/contact.html")

