from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from djangoratings.fields import RatingField
from django.db.models import Avg
from django.core.validators import MaxValueValidator,MinValueValidator



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

class Business(models.Model):
    banner_photo=models.ImageField(null=True,upload_to='businesses/banner/%Y/%m/%d')
    popularity_rating = models.IntegerField(null=True,default=0,
                                            validators=[MaxValueValidator(10),MinValueValidator(0)])

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


    def __unicode__(self):
        return self.name

    def get_no_reviews(self):
        return Review.objects.filter(business=self).count()
    def get_avg_rating(self):
        # get avg rating review for objects that were rated
        return Review.objects.filter(business=self,rating_score__range=(1,5)).aggregate(Avg('rating_score'))['rating_score__avg']

class Customer(models.Model):
    CHOICES = {
        ('B','Business'),
        ('C','Customer'),
    }
    user = models.OneToOneField(User)
    photo = models.FileField(null=True,upload_to='avatars/%Y/%m/%d',blank=True)
    user_type = models.CharField(choices=CHOICES,max_length=20,default='B')
    def __unicode__(self):
        return "%s %s" %(self.user.first_name,self.user.last_name)

class Review(models.Model):
    customer = models.ForeignKey(Customer,null=True)
    business = models.ForeignKey(Business,null=True)
    rating = RatingField(range=5,can_change_vote=True,allow_delete=True)
    review = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

class BusinessPhoto(models.Model):
    photo = models.ImageField(null=True,upload_to='businesses/%Y/%m/%d')
    #review = models.ForeignKey(Review,null=True)
    TYPE = (
        ('BP','BusinessPhoto'),
        ('RP','ReviewPhoto'),
        ('UP','UserPhoto')
    )
    business = models.ForeignKey(Business,null=True)
    photo_type = models.CharField(null=True,choices=TYPE,max_length=20)
    caption = models.CharField(null=True,max_length=100)

class Features(models.Model):
    name = models.CharField(max_length=255)
    def  __unicode__(self):
        return self.name

class EventCategory(models.Model):
    name = models.CharField(max_length=255)

class Event(models.Model):
    photo = models.ImageField(null=True,upload_to='events/%Y/%m/%d')
    name = models.CharField(max_length=20,null=True)
    categories= models.ManyToManyField(EventCategory)
    event_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    where = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    website_url = models.URLField(null=True)
    price = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name











