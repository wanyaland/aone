from __future__ import unicode_literals

from django.db import models
from core.config import CONTACTUS_REVIEW_STATUS


class EmailOutbox(models.Model):
    """
    Email warehouse
    """
    id = models.AutoField(primary_key=True)
    email_to = models.CharField(max_length=2048, help_text="comma separated emails")
    email_from = models.CharField(max_length=2048, help_text="comma separated emails")
    email_subject = models.CharField(max_length=2048)
    email_body = models.CharField(max_length=8000)
    email_attachment = models.CharField(max_length=2000, help_text="file attachment path")
    status = models.BooleanField(default=False, help_text="False: not sent, True: email sent")
    create_date = models.DateTimeField(auto_now_add=True, help_text="email insert date time")
    modify_date = models.DateTimeField(auto_now=True, help_text="email sent date time")

    class Meta:
        db_table = "EmailOutbox"


class ContactRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=400, null=False, blank=False)
    subject = models.CharField(max_length=500, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    review_status = models.CharField(max_length=100, choices=CONTACTUS_REVIEW_STATUS, default='OPEN')

    status = models.BooleanField(default=False, help_text="False: not sent, True: email sent")
    create_date = models.DateTimeField(auto_now_add=True, help_text="email insert date time")
    modify_date = models.DateTimeField(auto_now=True, help_text="email sent date time")

    def __unicode__(self):
        return "{} <{}> : {}".format(self.name, self.email, self.subject)

    class Meta:
        db_table = "ContactRequest"

