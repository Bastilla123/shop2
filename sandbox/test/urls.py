from django.urls import path, include

from .views import *


urlpatterns = [
    

    #Globalsettings
    path('edit/globalsettings/', GlobalsettingsUpdateView.as_view(),name="GlobalsettingsUpdateView"),

    #User CRUD
    path('list/user/', Userlistview.as_view(),
        name="Userlistview"),
    path("edit/user/<str:pk>/", UserUpdateView.as_view(),
        name="UserUpdateView"),

    path('create/user/', UserCreateView.as_view(),
        name="UserCreateView"),





]
