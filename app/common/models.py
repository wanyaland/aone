from __future__ import unicode_literals

from django.db import models


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
