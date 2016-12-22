from django.test import TestCase,RequestFactory
from models import Business,Review,ParentCategory,Category,ReviewTag
from django.contrib.auth.models import User,AnonymousUser
from django.conf import settings
from django.db import models
from geoposition.fields import Geoposition,GeopositionField
from django.test import LiveServerTestCase
from .views import tag_review
from tag_manager import TagManager
from ranking import ReviewRanking
from .models import ReviewTag
import json


class TagTest(TestCase):
    def setUp(self):
        self.tagger = TagManager()
        self.review = Review.objects.create()
        self.user = User.objects.create_user(username='harold',password='wanyama')
        self.user2 = User.objects.create_user(username='peter',password='nachwera')
        self.anonymous = AnonymousUser()

    def test_logged_user_can_tag_review(self):
        review_tag = self.tagger.add_tag(self.review,'COOL',self.user,'127.0.0.1')
        self.assertEqual(review_tag.tag,'COOL')

    def test_anonymous_can_tag(self):
        review_tag = self.tagger.add_tag(self.review,'HELPFUL',self.anonymous,'127.0.0.1')
        self.assertEqual(review_tag.tag,'HELPFUL')

    def test_one_vote_per_logged_user(self):
        self.tagger.add_tag(self.review,'COOL',self.user,'127.0.0.1')
        self.tagger.add_tag(self.review,'HELPFUL',self.user,'127.0.0.1')
        self.assertEqual(self.tagger.get_tag_votes(self.review),1)
        self.tagger.add_tag(self.review,'COOL',self.user2,'127.0.0.1')
        self.assertEqual(self.tagger.get_tag_votes(self.review),2)

    def test_one_vote_per_anonymous_user(self):
        self.tagger.add_tag(self.review,'COOL',self.anonymous,'127.0.0.1')
        self.tagger.add_tag(self.review,'HELPFUL',self.anonymous,'127.0.0.1')
        self.assertEqual(self.tagger.get_tag_votes(self.review),1)
        self.tagger.add_tag(self.review,'HEPFUL',self.anonymous,'127.0.0.2')
        self.assertEqual(self.tagger.get_tag_votes(self.review),2)

class TagViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='harold',password='wanyama')
        self.review = Review.objects.create()

    def test_view_can_tag(self):
        request = self.factory.post('/tag_review/',{'review_id':self.review.pk,'tag':'COOL'})
        request.user = self.user
        response = tag_review(request)
        review_tag = ReviewTag.objects.get(review=self.review)
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{'success':'true'})
        self.assertEqual(review_tag.tag,'COOL')

    def test_anonymous_tag(self):
        request = self.factory.post('/tag_review/',{'review_id':self.review.pk,'tag':'COOL'})
        request.user = AnonymousUser()
        response = tag_review(request)
        review_tag = ReviewTag.objects.get(review=self.review)
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{'success':'true'})
        self.assertEqual(review_tag.tag,'COOL')

class RankTest(TestCase):
    def setUp(self):
        self.review1 = Review(review='review1')
        self.review2 = Review(review='review2')
        self.ranking = ReviewRanking()
        self.business1 = Business(name='total',popularity_rating=4)
        self.business2 = Business(name='shell',popularity_rating=6)
        self.business1.save()
        self.business2.save()
        self.review1.business =  self.business1
        self.review2.business = self.business2
        self.review1.save()
        self.review2.save()
        self.review_tag1= ReviewTag(review=self.review1,tag='COOL',ip_address='127.0.0.1')
        self.review_tag2= ReviewTag(review=self.review2,tag='COOL',ip_address='127.0.0.2')
        self.review_tag1.save()
        self.review_tag2.save()

    def test_can_rank_reviews(self):
        '''
        formula = popularitypercent*0.60+markerspercent*0.40
        :return:
        '''
        rank1 = (0.5*0.6)+(0.4*0.4)
        rank2 = (0.5*0.6)+(0.6*0.4)
        self.assertEqual(self.ranking.get_rank(self.review1),rank1)
        self.assertEqual(self.ranking.get_rank(self.review2),rank2)



































