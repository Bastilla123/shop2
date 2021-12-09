from django.db import models
from django.contrib.auth.models import User
import os
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    vorname, extension = os.path.splitext(filename)
    thumb_extension = extension.lower()

    filename = str(uuid.uuid4()) + str(thumb_extension)


    return 'user_{0}/{1}'.format(instance.user_link.id, filename)


def validate_image(image):
    file_size = image.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit)

    #limit_mb = 3
    #if file_size > limit_mb * 1024 * 1024:
    #    raise ValidationError("Max size of file is %s MB" % limit_mb)

def user_directory_path(instance, *args,**kwargs):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if (instance is None):
        return

    filename = ""
    vorname, extension = os.path.splitext(filename)
    thumb_extension = extension.lower()

    filename = str(uuid.uuid4()) + str(thumb_extension)

    if (hasattr(instance.user_link,'id')):

        return '{2}_{0}/{1}'.format(instance.user_link.id, filename,instance.imagetype)
    elif (hasattr(instance.globalsettings_link,'id')):
        return '{2}_{0}/{1}'.format(instance.globalsettings_link.id, filename, instance.imagetype)

def print_kwargs(**kwargs):
    for key in kwargs:
        print("The key {} holds {} value".format(key, kwargs[key]))

class Photo(models.Model):
    file = models.ImageField(null=False,blank=False,default=" ")
    description = models.CharField(max_length=255, blank=True,default=" ")
    uploaded_at = models.DateTimeField(auto_now=True)
    from globalsettings.models import UserSettings
    user_link = models.OneToOneField(UserSettings, on_delete=models.CASCADE, null=True, blank=True,related_name="userimage")
    globalsettings_link = models.OneToOneField('globalsettings.Globalsettings', on_delete=models.CASCADE, null=True, blank=True)
    imagetype = models.PositiveSmallIntegerField(choices=((0, 'Benutzerbild'), (1, 'Firmenlogo'),), default=0,
                                                 null=False, blank=False)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


