from __future__ import division

from .models import ReviewTag
from tag_manager import TagManager


class Ranking(object):

    '''
    Review ranking factors:
    1.number of markers (cool,funny,helpful)-60% weight
    2.number of views
    3.business popularity-40% weight
    '''

    def __init__(self):
        self.tag_manager = TagManager

    def get_review_rank(self,review):
        '''
        currently does not include hits
        :param review:
        :return:
        '''
        total_number_of_tags = ReviewTag.objects.all().count()
        num_review_tags = ReviewTag.objects.filter(review=review).count()
        rank = (num_review_tags/total_number_of_tags)*0.6+(review.business.popularity_rating/10)*0.4
        return rank

    def get_rank_business(self,business):
        '''
        number of reviews
        average rating
        number of top reviews with a high ranking
        number of views
        :param business:
        :return:
        '''
        rank=0
        return rank

    def get_rank_events(self,event):
        '''
        number of comments
        number of views
        number of feedbacks
        :param event:
        :return:
        '''
        rank=0
        return rank









