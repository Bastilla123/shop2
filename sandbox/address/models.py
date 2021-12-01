from django.contrib.auth.models import Group
from django.db import models
from emailmarketing.choicesenum import *
from django.contrib.auth.models import User



import random

from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from emailmarketing.ModelMixins import Standard_Model_Mixin,LoggerModelMixin




#Merkmale
class Addressproperties(MPTTModel):
    name = models.CharField(max_length=32)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']




class Addresschoices(models.Model):
    choicename = models.TextField(default="",blank=False,null=False)
    fieldname = models.TextField(default="",blank=False,null=False)

    def __str__(self):
        return self.choicename

class UserRightsModelRelation(models.Model):

    user_link = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                    related_name="user_link")
    user_right_to_view = models.BooleanField(default=True)
    user_right_to_change = models.BooleanField(default=False)
    user_right_to_delete = models.BooleanField(default=False)

class GroupRightsModelRelation(models.Model):
    group_link = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                  related_name="group_link")
    group_right_to_view = models.BooleanField(default=True)
    group_right_to_change = models.BooleanField(default=False)
    group_right_to_delete = models.BooleanField(default=False)

class Address(LoggerModelMixin,Standard_Model_Mixin):
    #Stammdaten
    properties_link = models.ManyToManyField(Addressproperties, blank=True, default=None)
    customer_number = models.CharField(max_length=30, default="", blank=True, null=True)
    salutation = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                    related_name="address_salutation")
    title = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_title")
    firstname = models.CharField(max_length=255, default="", blank=True, null=True)
    lastname = models.CharField(max_length=255, default="", blank=True, null=True)

    companyname = models.CharField(max_length=255, default="", blank=True, null=True)
    companyname_extra = models.TextField(default=None, blank=True, null=True)
    street = models.CharField(max_length=255, default="", blank=True, null=True)
    zip = models.CharField(max_length=12, default="", blank=True, null=True)
    city = models.CharField(max_length=255, default="", blank=True, null=True)
    country = models.PositiveSmallIntegerField(choices=Country_Choices, blank=True, default=0, null=True)
    birthdate = models.DateField(default=None, blank=True, null=True)

    #Stammdaten 2
    salutation2 = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_salutation2")
    title2 = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                              related_name="address_title2")
    firstname2 = models.CharField(max_length=255, default="", blank=True, null=True)
    lastname2 = models.CharField(max_length=255, default="", blank=True, null=True)

    companyname2 = models.TextField(default=None, blank=True, null=True)
    companyname_extra2 = models.TextField(default=None, blank=True, null=True)
    street2 = models.CharField(max_length=255, default="", blank=True, null=True)
    zip2 = models.CharField(max_length=12, default="", blank=True, null=True)
    city2 = models.CharField(max_length=255, default="", blank=True, null=True)
    country2 = models.PositiveSmallIntegerField(choices=Country_Choices, blank=True, default=0, null=True)
    birthdate2 = models.DateField(default=None, blank=True, null=True)



    #Beruf
    employer = models.CharField(max_length=255, default="", blank=True, null=True)
    job_title = models.CharField(max_length=255, default="", blank=True, null=True)
    position_company = models.CharField(max_length=255, default="", blank=True, null=True)
    income = models.PositiveIntegerField(blank=True, default=0, null=True)
    employment_relationship = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_employment_relationship")

    #Kontakt
    homepage = models.CharField(max_length=255, default="", blank=True, null=True)
    letter_salutation = models.TextField(default=None, blank=True, null=True)
    preferred_contacttype = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True,
                                              default=None,
                                              related_name="address_preferred_contacttype2")

    #GWG
    gwg_contract_partner = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="contract_partner")
    gwg_birthname = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_birthdate = models.DateTimeField(default=None, blank=True, null=True)
    gwg_id_type = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="gwg_id_type")
    gwg_id_number = models.CharField(max_length=50, default="", blank=True, null=True)
    gwg_issuing_authority = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_nationality_authority = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_place_of_birth = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_abnormalities = models.TextField(default=None, blank=True, null=True)

    gwg_wb_beneficial_owner = models.BooleanField(default=False, null=True, blank=True)
    gwg_wb_firstname = models.CharField(max_length=255, default=None, blank=True, null=True)
    gwg_wb_lastname = models.CharField(max_length=255, default=None, blank=True, null=True)
    gwg_wb_street = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_wb_zip = models.CharField(max_length=12, default="", blank=True, null=True)
    gwg_wb_city = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_wb_nationality = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_wb_place_of_birth = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_wb_birthdate = models.DateField(default=None, blank=True, null=True)

    gwg_legal_form = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_registration_number = models.CharField(max_length=255, default="", blank=True, null=True)
    gwg_members_administrative_body = models.TextField(default=None, blank=True, null=True)

    #Verwaltung
    status1 = models.PositiveSmallIntegerField(choices=((0, 'Aktiv'),(1, 'Archiviert'),), blank=True, default=0, null=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_supervisor")
    contact_type = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_contact_type")
    origin_contact = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_origin_contact")
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_supervisor")
    tip_provider = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_tip_provider")

    terms_conditions_accepted =models.BooleanField(default=False,null=True,blank=True)
    recall_accepted = models.BooleanField(default=False, null=True, blank=True)
    vip = models.BooleanField(default=False, null=True, blank=True)
    customer_since =  models.DateField(blank=True, null=True,default=None)
    warning_notice = models.TextField(default=None, blank=True, null=True)
    dsgvo_status = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                       related_name="address_dsgvo_status")
    owned = models.ManyToManyField("estates.Estates", blank=True, null=True, default=None,
                                         related_name="address_owned")

    #Rights
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True,
                              related_name="%(class)s_owner", )
    user_rights_link = models.ManyToManyField(UserRightsModelRelation, default=None, blank=True,
                                         related_name="user_rights_link")
    group_rights_link = models.ManyToManyField(GroupRightsModelRelation, default=None, blank=True,
                                              related_name="group_rights_link")


    def __str__(self):

        return str(self.firstname)+" "+str(self.lastname)



class Telefax(Standard_Model_Mixin):

        address_link = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False, default=0,
                                         related_name="Telefax_address_link"
                                         )

        is_standard = models.BooleanField(default=True)
        eintrag = models.CharField(max_length=80, default="")


        def __str__(self):
            return self.eintrag

class Telefon(Standard_Model_Mixin):
        id = models.AutoField(primary_key=True)
        address_link = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False, default=0,related_name="Telefon_address_link"
                                         )
        is_standard = models.BooleanField(default=True)
        is_active = models.BooleanField(default=True)
        eintrag = models.CharField(max_length=80, default="")


        def __str__(self):
            return self.eintrag


class Email(Standard_Model_Mixin):

    address_link = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False, default=0,
                                     related_name="Email_address_link")


    eintrag = models.CharField(max_length=80, default="")

    is_standard = models.BooleanField(default=True)



    def __str__(self):
        return self.eintrag

class Emailsubscription(models.Model):

    subscription_status = models.PositiveSmallIntegerField(choices=subscription_status, blank=True, default=0,
                                                           null=True)  # status of subscription
    name = models.CharField(max_length=80, default="",primary_key=True)
    subscript_date = models.DateTimeField(blank=True, null=True,default=None)  # date on day by subscription
    ipadress_on_subscription = models.CharField(max_length=2000, default="",null=True,
                                                blank=True)  # store ip Adress by subscription date
    subscription_senddate = models.DateTimeField(blank=True, null=True, default=None)  # date on day by subscription
    subscription_confirmdate = models.DateTimeField(blank=True, null=True, default=None)  # date on day by subscription

    def __str__(self):
        return self.name



# Hier werden die Daten der individuellen Felder für Adressen reingeschrieben
class Addressindividualfields(Standard_Model_Mixin):

    fieldlist_link = models.ForeignKey("settings.IndividualFields", on_delete=models.SET_NULL, null=True,
                                       blank=True)  # Link zu dem individuellen Feld
    model_link = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True,
                                      blank=True)  # Link zu den Adressen

    integerfield = models.IntegerField(null=True,
                                               blank=True)  # Falls der Feldtyp Integer ist, dann wird hier geschrieben
    datumfield = models.DateTimeField(null=True, blank=True)  # Falls der Feldtyp Datum ist, dann wird hier geschrieben
    decimalfield = models.FloatField(null=True, blank=True)  # Falls der Feldtyp Dezimal ist, dann wird hier geschrieben
    charfield = models.CharField(null=True, blank=True,
                                 max_length=80)  # Falls der Feldtyp ein Varchar ist, dann wird hier geschrieben
    textfield = models.TextField(null=True, blank=True)  # Falls der Feldtyp ein Text ist dann wird hier geschrieben


# Hier werden die Selectsachen aus dem Adressenzusatz gespeichert
class Addressselect(Standard_Model_Mixin):
    individualfields_link = models.ForeignKey(Addressindividualfields, on_delete=models.CASCADE,related_name="Addressselect_choices",blank=True,null=True,default=None)  # Link auf den Adresszusatz
    choices_link = models.ForeignKey("settings.Choices", on_delete=models.CASCADE,blank=True,null=True,default=None)  # Link auf die Select Choices

class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return int(value) # return 0/1

def generate_token():
    return "".join(
        [
            random.choice("abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            for _ in range(160)
        ]
    )


class AuthToken(models.Model):
    token = models.CharField(max_length=200, default=generate_token, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    email = models.CharField(max_length=2000)


    @classmethod
    def delete_stale(cls):
        """Delete stale tokens, ie tokens that are more than TOKEN_DURATION seconds older."""
        cls.objects.filter(
            timestamp__lt=now() - timedelta(seconds=3600)
        ).delete()

    def __str__(self):
        return self.token
