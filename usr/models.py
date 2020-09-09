from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class TicketStatus(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    status_id = models.IntegerField()
    change_time = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_status'
        unique_together = (('ticket_id', 'status_id'),)


class TicketStatusHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    ticket_id = models.IntegerField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    change_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_status_history'


class Tickets(models.Model):
    priority_choices = (
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    ticket_id = models.AutoField(primary_key=True)
    issue_type = models.CharField(max_length=25, null=False)
    description = models.TextField(max_length=255, blank=True, null=False)
    finish_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=priority_choices,default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    assigned_to = models.IntegerField( blank=True, null=True)
    assigned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'
