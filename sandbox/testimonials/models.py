from django.db import models
from photo.models import Photo

# Create your models here.
class Testimonialmodel(models.Model):
    firstname = models.CharField(max_length=120, null=True, blank=True, default="")
    lastname = models.CharField(max_length=120, null=True, blank=True, default="")
    companyname = models.CharField(max_length=120, null=True, blank=True, default="")
    title = models.CharField(max_length=240, null=True, blank=True, default="")
    description = models.TextField(blank=True, default="", null=True)
    stars = models.PositiveSmallIntegerField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True,null=True, blank=True)
    image = models.OneToOneField(Photo, null=True, blank=True , on_delete=models.CASCADE)