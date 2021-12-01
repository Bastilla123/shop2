from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import MPTTModelAdmin


# Register your models here.

admin.site.register(Address)



