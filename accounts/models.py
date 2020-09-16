from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender_choices = [
        ('M','Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=2, choices=gender_choices, null=True, blank=True)
    contact_no = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    # def __str__(self):
        # return self.user.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()