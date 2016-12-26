from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import F
# Create your models here.

class Rank(models.Model):
    '''
    Takes a dictionary of parametes with corresponding weights and calculates rank
    '''
    def __init__(self,parameters):
        for key,value in parameters:
            rank = F(rank)+(key*value)

    content_type = models.ForeignKey(ContentType,related_name="rank")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    rank = models.FloatField(default=0)

    def __unicode__(self):
        return "%s with rank %d" %(self.content_object,self.rank)

    class Meta:
        ordering = ('-rank',)





