from django.test import TestCase,RequestFactory
from models import Business,Review,ParentCategory,Category,ReviewTag
from django.contrib.auth.models import User,AnonymousUser
from django.conf import settings
from django.db import models
from geoposition.fields import Geoposition,GeopositionField
from django.test import LiveServerTestCase
import json


class CoreTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory
        self.user = User.objects.create_user(username='harold',password='wanyama')
        self.review = Review()

    def test_logged_user_can_review(self):
        self.client.login(username='harold',password='wanyama')
        request = self.client.post('/tag_review/',{'review_id':self.review.id,'tag':'COOL'})
        self.assertJSONEqual(json.loads(request.content),{'success':'true'})
        self.assertEquals(self.review.reviewtag.tag,'COOL')


    def anonymous_user_can_review(self):
        response = self.client.post('/tag_review/',{'review_id':self.review.id,'tag':'COOL'})
        self.assertEqual(self.review.reviewtag,'COOL')
        self.assertJSONEqual(str(response.content),{u'success':u'true'})

    def logged_user_can_tag_once(self):
        pass

    def anonymous_user_can_tag_once(self):
        pass

    def user_can_tag_once(self):
        pass


















