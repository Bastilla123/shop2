from django import forms
from django.contrib.auth.models import User, Group
import django_filters
from address.models import *
from emailmarketing.Widget import CustomBooleanWidget



class AddressFilter(django_filters.FilterSet):

    firstname = django_filters.CharFilter(lookup_expr='icontains', label="Vorname")
    lastname = django_filters.CharFilter(lookup_expr='icontains', label="Nachname")
    is_active = django_filters.BooleanFilter(lookup_expr='icontains', label="Aktiv",widget=CustomBooleanWidget())



    class Meta:
        model = Address
        fields = ['lastname','firstname','is_active' ]


class EmailFilter(django_filters.FilterSet):

    eintrag = django_filters.CharFilter(lookup_expr='icontains', label="Email")

    class Meta:
        model = Email
        fields = ['eintrag' ]

class TelefonFilter(django_filters.FilterSet):

    eintrag = django_filters.CharFilter(lookup_expr='icontains', label="Telefonnummer")

    class Meta:
        model = Telefon
        fields = ['eintrag' ]

class TelefaxFilter(django_filters.FilterSet):

    eintrag = django_filters.CharFilter(lookup_expr='icontains', label="Telefaxnummer")

    class Meta:
        model = Telefax
        fields = ['eintrag' ]

