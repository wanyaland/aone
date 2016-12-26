from django.test import TestCase,RequestFactory
from models import Business,Review,ParentCategory,Category,\
    ReviewTag,Event,EventDiscussion,Customer
from django.contrib.auth.models import User,AnonymousUser
from django.conf import settings
from django.db import models
from geoposition.fields import Geoposition,GeopositionField
from django.test import LiveServerTestCase
from .views import tag_review,ReviewDetail,BusinessDetail,EventDetail,GetNearestBusinesses
from tag_manager import TagManager
from ranking import Ranking
from .models import ReviewTag
import json
from importlib import import_module
from django.core.files import File
import os


class HitCountTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='harold',password='wanyama')
        self.engine = import_module(settings.SESSION_ENGINE)
        self.store = self.engine.SessionStore()
        self.store.save()

    def test_business_detail_view(self):
        business = Business.objects.create(name='business')
        request = self.factory.get('/')
        request.session = self.store
        request.user = self.user
        response=BusinessDetail.as_view()(request,pk=business.pk)
        #self.assertEqual(response.context_data['hitcount']['pk'],business.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'],1)

    def test_review_detail_view(self):
        review = Review.objects.create(review='review')
        request = self.factory.get('/review_detail/')
        request.session = self.store
        request.user = self.user
        response = ReviewDetail.as_view()(request,pk=review.pk)
        self.assertEqual(review.hit_count.hits,1)

    def test_event_detail_view(self):
        event = Event.objects.create(name='event')
        self.assertEqual(event.hit_count.hits,0)
        request = self.factory.get('/event_detail/')
        request.session = self.store
        request.user = self.user
        response = EventDetail.as_view()(request,pk=event.pk)
        #self.assertEqual(response.context_data['hitcount']['pk'],event.pk)
        self.assertEqual(event.hit_count.hits,1)

class RankTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
        self.engine = import_module(settings.SESSION_ENGINE)
        self.store = self.engine.SessionStore()
        self.store.save()


    def test_can_rank_reviews(self):
        """
        parameters:weight
        number of views : 50%
        number of markers: 25%
        business popularity:25%
        :return:
        """
        request = self.factory.get('/')
        request.user = self.user
        request.session = self.store
        ReviewDetail.as_view()(request,pk=self.review1.pk)
        rank = (1*0.5)+(4*0.25)+(1*0.25)
        self.assertEqual(self.ranking.get_review_rank(self.review1),rank)
    def test_can_rank_businesses(self):
        """
        number of views :25%
        average rating : 50%
        number of reviews:25%
        :return:
        """
        request = self.factory.get('/')
        request.user = self.user
        request.session = self.store
        BusinessDetail.as_view()(request,pk=self.business2.pk)
        rank = (1*0.25)+(self.business2.get_avg_rating()*0.5)+(self.business2.get_no_reviews()*0.25)
        self.assertEqual(self.ranking.get_rank_business(self.business2),rank)

    def test_sort_businesses_by_rank(self):
        request = self.factory.get('/')
        request.session = self.store
        request.user = self.user
        BusinessDetail.as_view()(request,pk=self.business2.pk)
        (1*0.25)+(self.business2.get_avg_rating()*0.5)+(self.business2.get_no_reviews()*0.25)
        self.business1.get_avg_rating()*0.5+self.business1.get_no_reviews()*0.25
        businesses =[]
        businesses.append(self.business1)
        businesses.append(self.business2)
        self.assertEqual(businesses,[self.business1,self.business2])
        result = self.ranking.rank_businesses(businesses)
        self.assertEqual(result,[self.business2,self.business1])

    def test_can_rank_events(self):
        """
        number of comments :25%
        number of views:75%
        number of feedback:
        :return:
        """
        event = Event.objects.create(name='event')
        EventDiscussion.objects.create(customer=self.customer,event=event,comment='comment')
        EventDiscussion.objects.create(event=event,comment='comment',customer=self.customer)
        request = self.factory.get('/')
        request.user = self.user
        request.session = self.store
        EventDetail.as_view()(request,pk=event.pk)
        rank = 2*0.25+1*0.75
        self.assertEqual(self.ranking.get_rank_events(event),rank)

class BannerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.business1 = Business.objects.create(name="business1",web_address='http://business1.com')
        self.business1.banner = 'banner.jpg'
        self.business1.latitude = -149.8935557
        self.business1.longitude = 61.21759217
        self.business1.save()
        self.business2 = Business.objects.create(name='business2',web_address='http://business2.com')
        self.business2.latitude = -149.9054948
        self.business2.longitude = 61.19533942
        self.business2.banner = 'favicon.ico'
        self.business2.save()
        self.business3 = Business.objects.create(name='business3',latitude=-111.7714833,longitude=33.3354678,web_address='http://business3.com')
        self.business3.banner = 'banner3.jpg'
        self.business3.save()
        self.user = User.objects.create_user(username='harold',password='wanyama')
        self.customer = Customer.objects.get(user=self.user)

    def nearest_business(self):
        request = self.factory.post('/',{'latitude':-149.8935557,'longitude':61.21759217})
        response = GetNearestBusinesses.as_view()(request)
        expect ={
            "businesses":[{'Banner Image':self.business1.banner,'Business Name':self.business1.name,
                           'Business ID':self.business1.pk,'Business URL':self.business1.web_address},
                          {'Banner Image':self.business2.banner,'Business Name':self.business2.name,
                           'Business ID':self.business2.pk,'Business URL':self.business2.web_address}]
        }
        self.maxDiff=None
        self.assertEqual(str(response.content),expect)










































