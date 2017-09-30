"""
This module is used to insert analytics
and also provides methods to retrieve analytics


TODO: this class is not completed yet
need to add more implementation logic


TODO#1. Provide a pre_save and post_save signal functionality
"""
from app.business.models import Analytics


class AnalyticsWrapper(object):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        pass

    def save(self):
        """
        save analytics data
        and return analytic id
        :return: int
        """
        raise NotImplementedError()

    def load(self, id):
        """
        Load analytic data by Id
        return a dict (prefer)
        :param id:
        :return: return dict
        """
        raise NotImplementedError()

    def find(self, *kwargs):
        """
        find analytics data based on data passed
        :param kwargs:
        :return: a list of dict where each dict represents the analytics data
        """
        raise NotImplementedError()

    def save_from_request(self, request):
        """
        Retrieve information  from the request object and insert into analytics
        TODO: not implemented yet
        :param request:
        :return:
        """
        raise NotImplementedError()
