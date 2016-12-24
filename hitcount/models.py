from django.db import models
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

AUTH_USER_MODEL = getattr(settings,'AUTH_USER_MODEL','auth.User')
# Create your models here.
class HitCount(models.Model):
    hits = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField('object ID')
    content_object = GenericForeignKey('content_type','object_pk')

    class Meta:
        ordering = ('-hits',)
        get_latest_by = 'modified'
        verbose_name = _('hit count')
        verbose_name_plural = _('hit counts')

    def __unicode__(self):
        return '%s' %self.content_object

    def increase(self):
        self.hits = F(self.hits)+1
        self.save()

    def decrease(self):
        self.hits = F(self.hits)-1

    def hits_in_last(self,**kwargs):
        assert kwargs,'Must provide at least one time delta eg (days=1)'
        period = timezone.now() - timedelta(**kwargs)
        return self.hit_set.filter(created_gte=period).count()

class Hit(models.Model):
    created = models.DateTimeField(editable=False,auto_now_add=True,db_index=True)
    ip = models.CharField(max_length=40,editable=False)
    session = models.CharField(max_length=40,editable=False)
    user_agent = models.CharField(max_length=255,editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL,null=True,editable=False)
    hitcount = models.ForeignKey(HitCount,editable=False)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('hit')

    def __unicode__(self):
        return 'Hit %s:' % self.pk

    def save(self,*args,**kwargs):
        if self.pk is None:
            self.hitcount.increase()
        super(Hit,self).save(*args,**kwargs)

class HitCountMixin(object):
    """
    HitCountMixin provides an easy way to add a hit count property to your model
    """
    @property
    def hit_count(self):
        ctype=ContentType.objects.get_for_model(self.__class__)
        hit_count,created = HitCount.objects.get_or_create(
            content_type=ctype,object_pk=self.pk
        )
        return hit_count


