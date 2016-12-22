__author__ = 'Harold'

from .models import ReviewTag
from datetime import datetime

try:
    from django.utils.timezone import now
except:
    now = datetime.now

class TagManager(object):
    '''
    Manager that handles tagging reviews.
    Tagging can be done by authenticated and anonymous users
    '''
    def get_tag_votes(self,review):
        return ReviewTag.objects.filter(review=review).count()

    def get_total_tags(self):
        return ReviewTag.objects.all().count()

    def get_votes_by_tag(self,review,tag):
        return ReviewTag.objects.filter(review=review,tag=tag).count()

    def add_tag(self,review,tag,user,ip_address,cookie={}):
        kwargs = dict (
            review= review,
        )
        if user.is_anonymous() or user is None:
            kwargs['ip_address']=ip_address
        else:
            kwargs['user']=user
        try:
            review_tag = ReviewTag.objects.get(**kwargs)
        except ReviewTag.DoesNotExist:
            review_tag = ReviewTag.objects.create(**kwargs)
        review_tag.tag=tag
        review_tag.save()
        return review_tag












