from __future__ import division

from core.models import ReviewTag,EventDiscussion
from tag_manager import TagManager
from hitcount.models import HitCountMixin


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
        Use number of views in last
        currently does not include hits
        :param review:
        :return:
        '''
        number_of_reviews = review.hit_count.hits_in_last(days=7)
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
        rank = business.get_no_reviews()*0.25+business.get_avg_rating()*0.5+business.hit_count.hits_in_last(days=7)*0.25
        return rank

    def get_rank_events(self,event):
        '''
        number of comments
        number of views
        number of feedbacks
        :param event:
        :return:
        '''
        rank= EventDiscussion.objects.filter(event=event).count()*0.25+event.hit_count.hits_in_last(days=7)*0.75
        return rank

    def rank_businesses(self,businesses):
        businesses.sort(key=lambda x:self.get_rank_business(x),reverse=True)
        return businesses

    def rank_reviews(self,reviews):
        reviews.sort(key=lambda x:self.get_review_rank(x),reverse=True)
        return reviews

    def rank_events(self,events):
        events.sort(key=lambda x:self.get_rank_events(x),reverse=True)
        return events









