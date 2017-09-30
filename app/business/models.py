"""
This file hosts some common models required for the business



"""
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.managers import BusinessManager
from core.utils import get_slug
from core.config import CATEGORY_TYPES, USER_TYPES, BUSINESS, REVIEW_TAG_CHOICES, PHOTO_TAG, PHOTO_TYPE


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey("self", blank=True, null=True)
    category_type = models.CharField(max_length=20, default=BUSINESS, choices=CATEGORY_TYPES)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Category"


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, help_text="Country code ")
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Country"


class BusinessHour(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField()
    opening_hours = models.FloatField()
    closing_hours = models.FloatField()
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "BusinessHour"


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    banner_photo=models.ImageField(null=True,upload_to='businesses/banner/%Y/%m/%d')
    popularity_rating = models.IntegerField(null=True,default=0,
                                            validators=[MaxValueValidator(10),MinValueValidator(0)])

    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=100, null=False, blank=False)

    country = models.ForeignKey(Country,null=True)
    categories = models.ManyToManyField(Category)
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=50,null=True)
    phone_number = models.TextField(blank=True,null=True)
    web_address = models.URLField(null=True)
    photo = models.ImageField(null=True,upload_to='businesses/%Y/%m/%d')
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    approved = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    email = models.EmailField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    features = models.ManyToManyField('Feature', null=True)
    description = models.TextField(null=True)
    price_range = models.IntegerField(null=True)
    owner = models.ForeignKey('Customer', null=True)
    business_hours = models.ManyToManyField(BusinessHour)

    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    objects = BusinessManager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Business"

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = get_slug(self.name)
        return super(Business, self).save(*args, **kwargs)

    def get_no_reviews(self):
        return Review.objects.filter(business=self).count()

    def get_avg_rating(self):
        # get avg rating review for objects that were rated
        avg_rating = Review.objects.filter(business=self,rating_score__range=(1,5)).aggregate(Avg('rating_score'))['rating_score__avg']
        if avg_rating is None:
            return 0
        else:
            return avg_rating


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, unique=True)
    photo = models.FileField(null=True, upload_to='avatars/%Y/%m/%d',blank=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=20, default=BUSINESS)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    modify_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "Customer"

    @receiver(post_save,sender=User)
    def create_user_customer(sender,instance,created,**kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_customer(sender,instance,**kwargs):
        instance.customer.save()

    def __unicode__(self):
        return "%s  " %(self.user.username)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True)
    business = models.ForeignKey(Business, null=True)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review = models.TextField()
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.review

    class Meta:
        db_table = "Review"


class ReviewTag(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User,null=True,blank=True)
    ip_address = models.CharField(max_length=20)
    tag = models.CharField(choices=REVIEW_TAG_CHOICES, max_length=20)
    key = models.CharField(max_length=32,null=True)
    cookie = models.CharField(max_length=32,blank=True,null=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.user:
            return "%s tagged %s" %(self.user,self.tag)
        else:
            return "%s tagged %s" %(self.ip_address,self.tag)

    class Meta:
        db_table = "ReviewTag"


class BusinessPhoto(models.Model):

    id = models.AutoField(primary_key=True)
    photo = models.ImageField(null=True, upload_to='businesses/%Y/%m/%d')
    review = models.ForeignKey(Review, null=True)
    tag = models.CharField(max_length=20, choices=PHOTO_TAG, null=True)
    business = models.ForeignKey(Business, null=True)
    photo_type = models.CharField(null=True, choices=PHOTO_TYPE, max_length=20)
    caption = models.CharField(null=True, max_length=100)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "BusinessPhoto"


class Feature(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Feature"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(null=True, blank=True, upload_to='events/%Y/%m/%d')
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, null=True)
    categories= models.ManyToManyField(Category)
    event_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    where = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    website_url = models.URLField(null=True, blank=True)
    price = models.IntegerField(null=True)
    owner = models.ForeignKey(Customer, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Event"

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = get_slug(self.name)
        return super(Event, self).save(*args, **kwargs)


class EventDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.comment

    class Meta:
        db_table = "EventDiscussion"


class NewsCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "NewsCategory"


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    photo = models.ImageField(null=True, upload_to='news/%Y/%m/%d')
    content = models.TextField()
    category = models.ForeignKey(NewsCategory, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} - {}".format(self.title, self.category)

    class Meta:
        db_table = "News"


class Analytics(models.Model):
    """
    Trying to make is as general as possible
    """
    id = models.AutoField(primary_key=True)
    object_id = models.CharField(max_length=100, help_text="target object id , could be anything")
    object_model = models.CharField(max_length=100, help_text="object model")
    object_name = models.CharField(max_length=200, help_text="Item title or etc")
    object_visitor = models.CharField(max_length=200, help_text="logged in user identifier")
    object_visitor_type = models.CharField(max_length=200, help_text="logged in user type")

    other_data = models.CharField(max_length=8000, help_text="Other information related to the user or item, "
                                                             "prefer to insert json data here")

    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Analytics"

