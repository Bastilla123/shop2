from django.contrib.auth.models import Group
from django.db import models
#from emailmarketing.choicesenum import *
from django.contrib.auth.models import User



import random

from mptt.models import MPTTModel, TreeForeignKey
#from django.conf import settings
from bibliothek.ModelMixins import Standard_Model_Mixin,LoggerModelMixin




#Merkmale
class Addressproperties(MPTTModel):
    name = models.CharField(max_length=32)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    fieldname = models.CharField(max_length=80, default=None)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']




class Addresschoices(models.Model):
    choicename = models.TextField(default="",blank=False,null=False)
    fieldname = models.TextField(default="",blank=False,null=False)

    def __str__(self):
        return self.choicename

class Clientaddress(Standard_Model_Mixin):
    #Stammdaten
    interest_in_link = models.ManyToManyField(Addressproperties, blank=True, default=None,related_name="interest_in_link")
    properties_link = models.ManyToManyField(Addressproperties, blank=True, default=None,related_name="properties_link")
    customer_number = models.CharField(max_length=30, default="", blank=True, null=True)
    salutation = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                    related_name="address_salutation")
    title = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_title")
    firstname = models.CharField(max_length=255, default="", blank=True, null=True)
    lastname = models.CharField(max_length=255, default="", blank=False, null=False)

    companyname = models.CharField(max_length=255, default="", blank=True, null=True)
    companyname_extra = models.TextField(default=None, blank=True, null=True)
    street = models.CharField(max_length=255, default="", blank=True, null=True)
    zip = models.CharField(max_length=12, default="", blank=True, null=True)
    city = models.CharField(max_length=255, default="", blank=True, null=True)
    #country = models.PositiveSmallIntegerField(choices=Country_Choices, blank=True, default=0, null=True)
    birthdate = models.DateField(default=None, blank=True, null=True)


    #Beruf
    employer = models.CharField(max_length=255, default="", blank=True, null=True)
    job_title = models.CharField(max_length=255, default="", blank=True, null=True)
    position_company = models.CharField(max_length=255, default="", blank=True, null=True)
    income = models.PositiveIntegerField(blank=True, default=0, null=True)


    #Kontakt
    homepage = models.CharField(max_length=255, default="", blank=True, null=True)
    letter_salutation = models.TextField(default=None, blank=True, null=True)
    preferred_contacttype = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True,
                                              default=None,
                                              related_name="address_preferred_contacttype2")



    #Verwaltung



    origin_contact = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="address_origin_contact")


    terms_conditions_accepted =models.BooleanField(default=False,null=True,blank=True)
    recall_accepted = models.BooleanField(default=False, null=True, blank=True)
    newsletter_accept = models.BooleanField(default=False, null=False, blank=False)
    vip = models.BooleanField(default=False, null=True, blank=True)
    customer_since =  models.DateField(blank=True, null=True,default=None)
    warning_notice = models.TextField(default=None, blank=True, null=True)
    dsgvo_status = models.ForeignKey(Addresschoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                       related_name="address_dsgvo_status")





    def __str__(self):

        return str(self.firstname)+" "+str(self.lastname)



class Telefax(Standard_Model_Mixin):

        address_link = models.ForeignKey(Clientaddress, on_delete=models.CASCADE, blank=False, null=False, default=0,
                                         related_name="Telefax_address_link"
                                         )

        is_standard = models.BooleanField(default=True)
        eintrag = models.CharField(max_length=80, default="")


        def __str__(self):
            return self.eintrag

class Telefon(Standard_Model_Mixin):
        id = models.AutoField(primary_key=True)
        address_link = models.ForeignKey(Clientaddress, on_delete=models.CASCADE, blank=False, null=False, default=0,related_name="Telefon_address_link"
                                         )
        is_standard = models.BooleanField(default=True)
        is_active = models.BooleanField(default=True)
        eintrag = models.CharField(max_length=80, default="")


        def __str__(self):
            return self.eintrag


class Email(Standard_Model_Mixin):

    address_link = models.ForeignKey(Clientaddress, on_delete=models.CASCADE, blank=False, null=False, default=0,
                                     related_name="Email_address_link")


    eintrag = models.CharField(max_length=80, default="")

    is_standard = models.BooleanField(default=True)



    def __str__(self):
        return self.eintrag

class Emailsubscription(models.Model):

    #subscription_status = models.PositiveSmallIntegerField(choices=subscription_status, blank=True, default=0,
    #                                                       null=True)  # status of subscription
    name = models.CharField(max_length=80, default="",primary_key=True)
    subscript_date = models.DateTimeField(blank=True, null=True,default=None)  # date on day by subscription
    ipadress_on_subscription = models.CharField(max_length=2000, default="",null=True,
                                                blank=True)  # store ip Adress by subscription date
    subscription_senddate = models.DateTimeField(blank=True, null=True, default=None)  # date on day by subscription
    subscription_confirmdate = models.DateTimeField(blank=True, null=True, default=None)  # date on day by subscription

    def __str__(self):
        return self.name




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
