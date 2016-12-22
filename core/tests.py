from django.test import TestCase,RequestFactory
from models import Business,Review,ParentCategory,Category,\
    ReviewTag,ReviewView,BusinessView,Event,EventDiscussion,EventView,Customer
from django.contrib.auth.models import User,AnonymousUser
from django.conf import settings
from django.db import models
from geoposition.fields import Geoposition,GeopositionField
from django.test import LiveServerTestCase
from .views import tag_review,ReviewDetail
from tag_manager import TagManager
from ranking import Ranking
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
        self.review1 = Review(review='review1',rating_score=2)
        self.review2 = Review(review='review2',rating_score=3)
        self.ranking = Ranking()
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
        self.user = User.objects.create_user(username='harry',password='wanyama')
        self.customer = Customer.objects.get(user=self.user)

    def test_can_rank_reviews(self):
        '''
        formula = popularity*0.25+number of markers*0.25+number of views*0.5
        :return:
        '''
        review_view1 = ReviewView(review=self.review1,ip='127.0.0.1',session='session1')
        review_view2 = ReviewView(review=self.review2,ip='127.0.0.1',session='session2')
        review_view1.save()
        review_view2.save()
        rank1 = (1*0.25)+(4*0.25)+(1*0.5)
        rank2 = (1*0.25)+(6*0.25)+(1*0.5)
        self.assertEqual(self.ranking.get_review_rank(self.review1),rank1)
        self.assertEqual(self.ranking.get_review_rank(self.review2),rank2)

    def test_can_rank_businesses(self):
        '''
        number of reviews 25
        average rating 50
        number of top reviews with a high ranking ??
        number of views 25
        :return:
        '''
        BusinessView.objects.create(business=self.business1,ip='127.0.0.1',session='session1')
        BusinessView.objects.create(business=self.business2,ip='127.0.0.2',session='session2')
        rank1 = (1*0.25)+(2*0.5)+(1*0.25)
        rank2 = (1*0.25)+(3*0.5)+(1*0.25)
        self.assertEqual(self.ranking.get_rank_business(self.business1),rank1)
        self.assertEqual(self.ranking.get_rank_business(self.business2),rank2)

    def test_can_rank_events(self):
        '''
        number of comments 25%
        number of views   75%
        number of feedbacks
        :return:
        '''
        event1 = Event.objects.create(name='event1')
        event2 = Event.objects.create(name='event2')
        EventDiscussion.objects.create(customer=self.customer,event=event1,comment='comment')
        EventDiscussion.objects.create(event=event1,comment='comment',customer=self.customer)
        EventDiscussion.objects.create(event=event2,comment='comment',customer=self.customer)

        EventView.objects.create(event=event1,ip='127.0.0.1',session='session')
        EventView.objects.create(event=event2,ip='127.0.0.2',session='session2')

        rank1 = 2*0.25+1*0.75
        rank2 = 1*0.25+1*0.75

        self.assertEqual(self.ranking.get_rank_events(event1),rank1)
        self.assertEqual(self.ranking.get_rank_events(event2),rank2)









































