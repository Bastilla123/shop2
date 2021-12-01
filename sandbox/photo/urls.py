
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('uploadphoto/<int:imagetype>', photo_list,name="uploadphoto"), #imagetype 0 = Userfoto imagetyp 1 = Logo
    path('delete/photo/<int:id>', deletephoto,name="deletephoto"),
]