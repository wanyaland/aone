from __future__ import division

from .models import ReviewTag,ReviewView,BusinessView,EventDiscussion,EventView
from tag_manager import TagManager


class Ranking(object):

    '''
    Review ranking factors:
    1.number of markers (cool,funny,helpful)-25% weight
    2.number of views  - 50% weight
    3.business popularity-25% weight
    '''

    def __init__(self):
        self.tag_manager = TagManager

    def get_review_rank(self,review):
        '''
        currently does not include hits
        :param review:
        :return:
        '''
        number_of_reviews = ReviewView.objects.filter(review=review).count()
        num_review_tags = ReviewTag.objects.filter(review=review).count()
        rank = num_review_tags*0.25+review.business.popularity_rating*0.25+number_of_reviews*0.5
        return rank

    def get_rank_business(self,business):
        '''
        number of reviews 25
        average rating 50
        number of top reviews with a high ranking
        number of views 25
        :param business:
        :return:
        '''
        rank = business.get_no_reviews()*0.25+business.get_avg_rating()*0.5+(BusinessView.objects.filter(business=business).count())*0.25
        return rank

    def get_rank_events(self,event):
        '''
        number of comments
        number of views
        number of feedbacks
        :param event:
        :return:
        '''
        rank= EventDiscussion.objects.filter(event=event).count()*0.25+EventView.objects.filter(event=event).count()*0.75
        return rank









