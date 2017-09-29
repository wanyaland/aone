from analytics import AnalyticsWrapper


class MasterMiddleware(object):
    """
    Instead of having multiple middleware, create a middleware with different utility methods
    TODO: this is not completed yet
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response
        return response

    def insert_analytics(self, request):
        """
        insert analytics here

        :return:
        """
        raise NotImplementedError()
