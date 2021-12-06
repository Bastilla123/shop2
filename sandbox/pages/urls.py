from django.urls import path, include

from .views import *

urlpatterns = [


    path('impressum/', impressumview, name="impressumview"),
    path('godb/', gobdview, name="godb"),
    path('revisionssicherheit/', revisionssicherheitview, name="revisionssicherheitview"),

]
app_name = 'pages'