from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tickets(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    issue_type = models.CharField(max_length=25, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)
    finish_date = models.DateField(blank=False, null=False)
    priority = models.CharField(max_length=10, blank=False, null=False)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, related_name='user_id')
    created_at = models.DateTimeField(blank=False, null=False)
    assigned_to = models.ForeignKey(User, db_column='assigned_to', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='assigned_to')
    assigned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'