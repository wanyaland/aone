__author__ = 'Harold'
from django.apps import AppConfig
from actstream import registry
from django.contrib.auth.models import User

class MyAppConfig(AppConfig):
    name='core'
    def ready(self):
        registry.register(User,self.get_model('Business'),self.get_model('Event'),self.get_model('Review'),self.get_model('BusinessPhoto'),self.get_model('ReviewTag'))
