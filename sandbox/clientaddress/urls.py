from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.conf.urls import url



urlpatterns = [


    path('list/address/', views.AddressListView.as_view(), name="addresslist"),  # Liste aller Addressen

    url(r"^edit/Address/(?P<pk>.*)/$", views.AddressUpdateView.as_view(),name="AddressUpdateView"),
    url(r"^edit/address/(?P<pk>.*)/$", views.AddressUpdateView.as_view(),name="AddressUpdateView"),
    url(r"^create/address/$", views.AddressCreateView.as_view(),name="AddressCreateView"),
    #url(r"^create/address2/$", views.AddressCreateView2.as_view(),name="AddressCreateView"),
    url(r'^$', views.AddressListView.as_view(), name="home"),  # Liste aller Addressen
    url(r"^delete/address/(?P<pk>\d+)/$", views.DeleteAddressView.as_view() ,name="delete_address",), #Löscht eine Adresse
    url(r"^delete/Address/(?P<pk>\d+)/$", views.DeleteAddressView.as_view() ,name="delete_address",), #Löscht eine Adresse


    url(r'^subscriptionactivate/([0-9A-Za-z]*)/$',
        views.subscriptionactivate, name='subscriptionactivate'),

    #Newsletter
    path('submitnewsletter/', views.submitnewsletter, name='submitnewsletter'),
    path('validate/', views.validate_email, name='validate_email'),

    #Contactform
    path('submitcontact/', views.submitcontactform, name='submitcontactform'),


    #Email CRUD
    path("list/email/<int:addressid>/", views.EmailListView.as_view(),
        name="EmailListView_emailid"),
    url(r'^list/email/$', views.EmailListView.as_view(),
        name="EmailListView"),
    path("edit/email/<str:pk>/", views.EmailUpdateView.as_view(),
        name="EmailUpdateView"),
    path("edit/Email/<str:pk>/", views.EmailUpdateView.as_view(),
        name="EmailUpdateView"),
    url(r'^create/email/$', views.EmailCreateView.as_view(),
        name="AddressEmailCreateView"),
    path('delete/email/<str:pk>/', views.EmailDeleteView.as_view(),
        name="EmailDeleteView"),


    #Telefon CRUD
    path("list/telefon/<int:addressid>/", views.TelefonListView.as_view(),
        name="TelefonListView_adressid"),
    url(r'^list/telefon/$', views.TelefonListView.as_view(),
        name="TelefonListView"),
    path("edit/Telefon/<str:pk>/", views.TelefonUpdateView.as_view(),
        name="TelefonUpdateView"),
    url(r'^create/telefon/$', views.TelefonCreateView.as_view(),
        name="TelefonCreateView"),
    path('delete/telefon/<str:pk>/', views.TelefonDeleteView.as_view(),
        name="TelefonDeleteView"),

    #Telefax CRUD
    path("list/telefax/<int:addressid>/", views.TelefaxListView.as_view(),
        name="TelefaxListView_adressid"),
    url(r'^list/telefax/$', views.TelefaxListView.as_view(),
        name="TelefaxListView"),
    path("edit/telefax/<str:pk>/", views.TelefaxUpdateView.as_view(),
        name="TelefaxUpdateView"),
    url(r'^create/telefax/$', views.TelefaxCreateView.as_view(),
        name="TelefaxCreateView"),
    path('delete/telefax/<str:pk>/', views.TelefaxDeleteView.as_view(),
        name="TelefaxDeleteView"),


]