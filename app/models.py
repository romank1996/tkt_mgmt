# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    ticket_id = models.IntegerField(primary_key=True)
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



class TicketAssignHistory(models.Model):
    ticket_id = models.IntegerField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, db_column='assigned_to',on_delete=models.DO_NOTHING,blank=True, null=True)
    assigned_time = models.DateTimeField(blank=True, null=True)
    assigned_by = models.ForeignKey(User, db_column='assigned_by',on_delete=models.DO_NOTHING,blank=True, null=True,related_name='assigned_by')

    class Meta:
        managed = False
        db_table = 'ticket_assign_history'


class TicketStatusHistory(models.Model):
    ticket_id = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey(Status,db_column='status_id',on_delete=models.DO_NOTHING, blank=True, null=True)
    change_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(User, db_column='modified_by',on_delete=models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_status_history'


class Faqs(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faqs'