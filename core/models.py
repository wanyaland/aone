from django.db import models
from django.contrib.auth.models import User
#from geoposition.fields import GeopositionField
from djangoratings.fields import RatingField
from django.db.models import Avg
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from hitcount.models import HitCountMixin,HitCount
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from .managers import BusinessManager

AUTH_USER_MODEL = getattr(settings,'AUTH_USER_MODEL','auth.User')

# Create your models here.
class ParentCategory(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40,null=True)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40)
    parent_category = models.ForeignKey(ParentCategory,blank=True,null=True)
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class BusinessHours(models.Model):
    day = models.IntegerField()
    opening_hours = models.FloatField()
    closing_hours = models.FloatField()

class Business(models.Model,HitCountMixin):
    banner_photo=models.ImageField(null=True,upload_to='businesses/banner/%Y/%m/%d')
    popularity_rating = models.IntegerField(null=True,default=0,
                                            validators=[MaxValueValidator(10),MinValueValidator(0)])
    hit_count_generic = GenericRelation(
        HitCount,object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country,null=True)
    categories = models.ManyToManyField(Category)
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=50,null=True)
    phone_number = models.TextField(blank=True,null=True)
    web_address = models.URLField(null=True)
    photo = models.ImageField(null=True,upload_to='businesses/%Y/%m/%d')
    create_date = models.DateTimeField(auto_now_add=True,null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    approved = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    email = models.EmailField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    features = models.ManyToManyField('Features',null=True)
    description = models.TextField(null=True)
    price_range = models.IntegerField(null=True)
    owner = models.ForeignKey('Customer',null=True)
    business_hours = models.ManyToManyField(BusinessHours)

    objects = BusinessManager()

    def __unicode__(self):
        return self.name

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
    BUSINESS='B'
    CUSTOMER='C'
    MODERATOR='M'
    CHOICES = {
        (BUSINESS,'Business'),
        (CUSTOMER,'Customer'),
        (MODERATOR,'Moderator'),
    }
    user = models.OneToOneField(User)
    photo = models.FileField(null=True,upload_to='avatars/%Y/%m/%d',blank=True)
    user_type = models.CharField(choices=CHOICES,max_length=20,default=BUSINESS)
    @receiver(post_save,sender=User)
    def create_user_customer(sender,instance,created,**kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save,sender=User)
    def save_user_customer(sender,instance,**kwargs):
        instance.customer.save()

    def __unicode__(self):
        return "%s  " %(self.user.username)


class Review(models.Model,HitCountMixin):
    customer = models.ForeignKey(Customer,null=True)
    hit_count_generic = GenericRelation(
        HitCount,object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    business = models.ForeignKey(Business,null=True)
    rating = RatingField(range=5,can_change_vote=True,allow_delete=True)
    review = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.review


class ReviewTag(models.Model):
    CHOICES ={
        ('C','COOL'),
        ('H','HELPFUL'),
        ('F','FUNNY'),
    }
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User,null=True,blank=True)
    ip_address = models.CharField(max_length=20)
    tag = models.CharField(choices=CHOICES,max_length=20)
    key = models.CharField(max_length=32,null=True)
    date_added = models.DateField(default=datetime.now,editable=False)
    date_changed = models.DateField(default=datetime.now,editable=False)
    cookie = models.CharField(max_length=32,blank=True,null=True)


    def __unicode__(self):
        if self.user:
            return "%s tagged %s" %(self.user,self.tag)
        else:
            return "%s tagged %s" %(self.ip_address,self.tag)



class BusinessPhoto(models.Model):
    photo = models.ImageField(null=True,upload_to='businesses/%Y/%m/%d')
    #review = models.ForeignKey(Review,null=True)
    BUSINESSPHOTO='BP'
    REVIEWPHOTO ='RP'
    USERPHOTO = 'UP'
    TYPE = (
        (BUSINESSPHOTO,'BusinessPhoto'),
        (REVIEWPHOTO,'ReviewPhoto'),
        (USERPHOTO,'UserPhoto')
    )
    TAG_HELPFUL='H'
    TAG_INAPPROPRIATE='I'
    TAG =(
        (TAG_HELPFUL,'Helpful'),
        (TAG_INAPPROPRIATE,'Inappropriate'),
    )
    tag = models.CharField(max_length=20,choices=TAG,null=True)
    business = models.ForeignKey(Business,null=True)
    photo_type = models.CharField(null=True,choices=TYPE,max_length=20)
    caption = models.CharField(null=True,max_length=100)
    created = models.DateTimeField(auto_now_add=True,default=datetime.now())

class Features(models.Model):
    name = models.CharField(max_length=255)
    def  __unicode__(self):
        return self.name

class EventCategory(models.Model):
    name = models.CharField(max_length=255)

class Event(models.Model,HitCountMixin):
    photo = models.ImageField(null=True,upload_to='events/%Y/%m/%d')
    hit_count_generic = GenericRelation(
        HitCount,object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    name = models.CharField(max_length=20,null=True)
    categories= models.ManyToManyField(EventCategory)
    event_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    where = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    website_url = models.URLField(null=True)
    price = models.IntegerField(null=True)
    owner = models.OneToOneField(Customer,null=True)

    def __unicode__(self):
        return self.name

class EventDiscussion(models.Model):
    customer = models.ForeignKey(Customer)
    comment = models.TextField()
    date = models.DateField(auto_now=True)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.comment











