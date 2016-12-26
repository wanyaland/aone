from django.test import TestCase
from core.models import Business

from .models import Rank

# Create your tests here.

class RankTest(TestCase):
    def setUp(self):
        self.business = Business.objects.create(name='business')
        self,rank = Rank()

