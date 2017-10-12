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
from core.config import *


class ListingFaq(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1024, null=False, blank=False)
    answer = models.TextField(null=False, blank=False)

    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ListingFaq"

    def __unicode__(self):
        return self.question


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    icon = models.FileField(upload_to="categories/icon/", null=True, blank=True)
    slug = models.CharField(max_length=500, null=True, blank=True)
    parent_category = models.ForeignKey("self", blank=True, null=True)
    category_type = models.CharField(max_length=20, default=BUSINESS, choices=CATEGORY_TYPES)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug_raw_value = (self.parent_category and (self.parent_category.name+'-> ') or '') + self.name
        self.slug = get_slug(slug_raw_value, unique=False)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = "Category"
        verbose_name_plural = "Categories"


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, help_text="Country code", unique=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Country"


class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.country.name+": "+self.name

    class Meta:
        db_table = "City"


class BusinessHour(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=10, choices=WEEKDAYS)
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "BusinessHour"

    def __unicode__(self):
        return "{} :: Open:{},  Close: {}".format(self.day, self.opening_hours, self.closing_hours)


class FileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_upload_type = models.CharField(max_length=200, null=False, blank=False,
                                        choices=FILE_UPLOAD_PATH,
                                        default=FILE_UPLOAD_PATH[0][0])
    file_path = models.FileField()

    def save(self, *args, **kwargs):
        self.file_path.upload_to = self.file_upload_type
        super(FileUpload, self).save(*args, **kwargs)

    class Meta:
        db_table = 'FileUpload'

    def __unicode__(self):
        return "{}: {}".format(self.file_name, self.file_upload_type)


class Business(models.Model):
    id = models.AutoField(primary_key=True)
    banner_photo = models.ImageField(null=True, upload_to='businesses/banner/%Y/%m/%d')
    popularity_rating = models.IntegerField(null=True, default=0,
                                            validators=[MaxValueValidator(10),MinValueValidator(0)],
                                            help_text="Rating, max 10 min 0")

    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=500, null=True, blank=True)

    categories = models.ManyToManyField(Category)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=100)
    web_address = models.URLField(null=True, help_text="website url")
    photo = models.ImageField(null=True, upload_to='businesses/%Y/%m/%d')
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    email = models.EmailField(null=True)
    start_time = models.TimeField(null=True, help_text="Listing start time", blank=True)
    end_time = models.TimeField(null=True, help_text="Listing end time", blank=True)
    features = models.ManyToManyField('Feature', help_text="Add features", blank=True)
    description = models.TextField(null=True, blank=True)
    price_min = models.IntegerField(null=True, help_text="min price")
    price_max = models.IntegerField(null=True, help_text="max price")
    owner = models.ForeignKey('Customer', null=True)
    business_hours = models.ManyToManyField(BusinessHour)
    video_url = models.URLField(blank=True, null=False)
    exclusive = models.BooleanField(default=False)

    faq = models.ManyToManyField(ListingFaq, blank=True)

    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    objects = BusinessManager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Business"

    def save(self, *args, **kwargs):
        old_slug = self.slug
        if (not kwargs.get('refresh')) and (not old_slug):
            self.slug = get_slug(self.name)
        return super(Business, self).save(*args, **kwargs)

    def get_no_reviews(self):
        return Review.objects.filter(business=self).count()

    def get_avg_rating(self):
        # get avg rating review for objects that were rated
        avg_rating = Review.objects.filter(business=self, rating_score__range=(1,5)).aggregate(Avg('rating_score'))['rating_score__avg']
        if avg_rating is None:
            return 0
        else:
            return avg_rating


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, unique=True)
    photo = models.FileField(null=True, upload_to='avatars/%Y/%m/%d', blank=True)
    user_type = models.CharField(choices=USER_TYPES, max_length=20, default=BUSINESS)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    modify_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "Customer"

    @receiver(post_save,sender=User)
    def create_user_customer(sender, instance,created,**kwargs):
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
    attachment = models.FileField(upload_to="review_attachment", null=True, blank=True)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    title = models.CharField(max_length=500, null=False, blank=False)
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
    user = models.ForeignKey(User, null=True, blank=True)
    ip_address = models.CharField(max_length=20)
    tag = models.CharField(choices=REVIEW_TAG_CHOICES, max_length=20)
    key = models.CharField(max_length=32, null=True)
    cookie = models.CharField(max_length=32, blank=True, null=True)
    #user_agent = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s tagged %s" %(self.tag, self.review)

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