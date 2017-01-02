__author__ = 'Harold'

from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from actstream.managers import ActionManager,stream
from django.db import models
from geopy.geocoders import Nominatim

class MyActionManager(ActionManager):
    @stream
    def mystream(self,obj,verb='posted',time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb=verb,timestamp__lte=time)


class BusinessManager(models.Manager):

    def search_business(self,location):
        geolocator = Nominatim()
        place = geolocator.geocode(location)
        qs = self.distance(place.latitude,place.longitude)
        return qs
    '''
    def geosearch(self, query):
        """
        Returns a queryset sorted by geographic proximity to the query.

        The geosearch method depends on a raw query, so it must sanitize all
        its inputs without relying on Django to protect from SQL injection
        attacks.

        :param query: The location against which to search, either represents
            a postal code or latitude and longitude
        :type query: Either a string or a tuple
        """
        try:
            latitude, longitude = query.split(',')
        except ValueError:
            # Possibly a zip code?
            postal_code = query[:5]
            try:
                postal_area = PostalCode.objects.get(code=postal_code)
            except PostalCode.DoesNotExist:
                # No such postal code, dolts!
                # TODO: there should be a warning somewhere about this, perhaps
                # a message sent to the user?
                return self.get_query_set().all()
            else:
                latitude, longitude = postal_area.latitude, postal_area.longitude
        else:
            latitude, longitude = float(latitude), float(longitude)
        return self.distance(latitude, longitude)
        '''
    def distance(self,latitude,longitude):
        """
        Return a queryset of businesses annotated with their distance from the given point
        Coefficients represent great cirlce measurements. Options include
            3956 - miles
            6371 - kilometers

        http://www.benamy.info/guides/haversine-formula-distance-query-with-django-postgresql
        :param latitude:
        :param longitude:
        :return:
        """
        coefficient = 3959
        return self.get_query_set().extra(select={
            "distance": "%s * acos(cos(radians(%s)) * cos(radians(latitude)) "
                        "* cos(radians(longitude) - radians(%s)) + "
                        "sin(radians(%s)) * sin(radians(latitude)))"},
                select_params=(coefficient, latitude, longitude,
                    latitude)).order_by('distance')


