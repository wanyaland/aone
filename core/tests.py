from django.test import TestCase
from models import Business,Review,ParentCategory,Category
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from geoposition.fields import Geoposition,GeopositionField
from django.test import LiveServerTestCase
from selenium import webdriver



class CoreTestCase(LiveServerTestCase):

    def setUp(self):
        self.business = Business()
        self.business_one = Business.objects.create(name="one")
        self.business_two = Business.objects.create(name="two")
        self.business_three = Business.objects.create(name="three")
        self.business_four = Business.objects.create(name="four")
        self.review_one = Review.objects.create(business=self.business_one,rating_score=3)
        self.review_two = Review.objects.create(business=self.business_two,rating_score=2)
        self.review_three = Review.objects.create(business=self.business_three,rating_score=5)
        self.parent_category = ParentCategory.objects.create(name='parent_category')
        self.category = Category.objects.create(parent_category=self.parent_category,name='cat')
        self.business_one.categories.add(self.category)
        self.business_two.categories.add(self.category)
        self.business_three.categories.add(self.category)
        self.selenium = webdriver.Chrome("C:/Users/Harold/Downloads/chromedriver.exe")
        super(CoreTestCase,self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(CoreTestCase,self).tearDown()

    def test_can_get_businesses(self):
        selenium = self.selenium
        self.business_one.latitude = 18.288319
        self.business_one.longitude = -67.13604
        self.business_two.latitude = 18.279531
        self.business_two.longitude = -66.80217
        self.business_three.latitude = 43.005895
        self.business_three.longitude = -71.013202
        self.business_one.save()
        self.business_two.save()
        self.business_three.save()

        response = selenium.get('/get_nearest_businesses/',)
        self.assertEquals(response.status_code,200)





'''
class CoreTestCase(TestCase):

    def setUp(self):
        self.business = Business()
        self.business_one = Business.objects.create(name="one")
        self.business_two = Business.objects.create(name="two")
        self.business_three = Business.objects.create(name="three")
        self.business_four = Business.objects.create(name="four")
        self.review_one = Review.objects.create(business=self.business_one,rating_score=3)
        self.review_two = Review.objects.create(business=self.business_two,rating_score=2)
        self.review_three = Review.objects.create(business=self.business_three,rating_score=5)
        self.parent_category = ParentCategory.objects.create(name='parent_category')
        self.category = Category.objects.create(parent_category=self.parent_category,name='cat')
        self.business_one.categories.add(self.category)
        self.business_two.categories.add(self.category)
        self.business_three.categories.add(self.category)

    def test_can_save_negative_string(self):
        latitude=-26.206820
        longitude = 28.038800
        self.business.id = 1
        self.business.location = Geoposition(latitude,longitude)
        self.business.save()
        self.assertEquals(self.business.id,1)

    def test_can_find_nearest_businesses(self):
        self.business_one.latitude = 18.288319
        self.business_one.longitude = -67.13604
        self.business_two.latitude = 18.279531
        self.business_two.longitude = -66.80217
        self.business_three.latitude = 43.005895
        self.business_three.longitude = -71.013202
        self.business_one.save()
        self.business_two.save()
        self.business_three.save()
        response = self.client.post('/get_nearest_businesses/',
                                    {'latitude':18.288319,'longitude':-67.13604})
        self.assertEquals(response.status_code,200)
        print response.content

    def test_can_get_top_businesses(self):
        response = self.client.post('/get_home_page_businesses/',{'parent_id':self.parent_category.id})
        self.assertEquals(response.status_code,200)
        print response.content




'''













