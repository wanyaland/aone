from __future__ import unicode_literals

from django.db import models


class ContactUsRequest(models.Model):
    name = models.CharField(max_length=1024, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=1024, null=False, blank=False)
    message = models.CharField(max_length=8000)
    read_by = models.CharField(max_length=500, default=False, help_text="Boolean field to indicate if the contact request is read by someone or not, 0-> unread, 1-> read")
    reader_comments = models.CharField(max_length=4000, help_text="Comments by reader of this contact request")

    create_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    update_date = models.DateTimeField(null=False, blank=False, auto_now=True)

    class Meta:
        db_table = 'ContactUsRequest'
