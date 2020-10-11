# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Status(models.Model):
    status_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class Tickets(models.Model):
    priority_choices = (
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    ticket_id = models.AutoField(primary_key=True)
    issue_type = models.CharField(max_length=25, blank=False, null=False)
    description = models.TextField(max_length=255, blank=False, null=False)
    finish_date = models.DateField(blank=False, null=False)
    priority = models.CharField(max_length=10, choices=priority_choices,default='medium')
    user = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False, related_name='created_by')
    created_at = models.DateTimeField(blank=False, null=False)
    assigned_to = models.ForeignKey(User, limit_choices_to={'groups__name': "engineer"}, db_column='assigned_to', on_delete=models.DO_NOTHING, blank=True, null=True, related_name="assigned")
    assigned_at = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(Status, db_column='status_id', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_closed = models.BooleanField(null=True,default=False,blank=True)

    class Meta:
        managed = False
        db_table = 'tickets'

class TicketStatusHistory(models.Model):
    ticket_id = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey(Status,db_column='status_id',on_delete=models.DO_NOTHING, blank=True, null=True)
    change_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, db_column='modified_by',on_delete=models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ticket_status_history'


class Faqs(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'faqs'

    def get_absolute_url(self):
        return reverse("faq")