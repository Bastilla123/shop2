from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Globalsettings(models.Model):
    client_companyname = models.CharField(max_length=240, null=True, blank=True, default="")
    client_city = models.CharField(max_length=240, null=True, blank=True, default="")
    client_street = models.CharField(max_length=240, null=True, blank=True, default="")
    client_zip = models.IntegerField(null=True, blank=True, default=0)
    client_country = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    impressum = models.TextField(blank=True, default="", null=True)

class UserSettings(models.Model):
    user_link = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name="usersettings_user_link", primary_key=True, )
    street = models.CharField(max_length=120, default="", blank=True, null=True)
    zip = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    city = models.CharField(max_length=120, default="", blank=True, null=True)

    birthdate = models.DateField(default=None, blank=True, null=True)
    company_position = models.CharField(max_length=240, default="", blank=True, null=True)
    description = models.TextField(blank=True, default="", null=True)

    #Social Media
    facebook_url = models.CharField(max_length=240, default="", blank=True, null=True)
    instagram_url = models.CharField(max_length=240, default="", blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user_link=instance)