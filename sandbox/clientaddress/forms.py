from django.urls import reverse
from bibliothek.FormMixins import StandardMixin

from django import forms

from .models import *
from bibliothek.Widgets import *
#from bibliothek.choicesenum import *


def replacestringinlist(list,searchstring,replacestring):
    for n, i in enumerate(list):

        if i == searchstring:
            list[n] = replacestring

def recursive_node_to_dict(node):

    return {

        'name': node.name, 'id': node.pk,
         # Notice the use of node._cached_children instead of node.get_children()
        'subs' : [recursive_node_to_dict(c) for c in node._cached_children]
    }

def test(node):
    import json
    from mptt.templatetags.mptt_tags import cache_tree_children
    subTrees = cache_tree_children(node.get_descendants(include_self=True))
    subTreeDicts = []
    for subTree in subTrees:
        subTree = recursive_node_to_dict(subTree)
        subTreeDicts.append(subTree)
    jsonTree = json.dumps(subTreeDicts, indent=4)
    # optional clean up, remove the [ ] at the beginning and the end, its needed for D3.js
    jsonTree = jsonTree[1:len(jsonTree)]
    jsonTree = jsonTree[:len(jsonTree) - 1]
    return jsonTree

def listtocommaseperated(list):
    string = ""
    counter = 0
    for entry in list:
        if counter == 0:
            string += str(entry)
        else:
            string += ","+str(entry)
        counter += 1

    return string

def getliste():
    Fieldlistmappingobjects = Field_to_box_mapping.objects.filter(modul=0, submodul=0, aktiv=True).order_by(
        "box_link",
        "position")
    liste = []
    if (Fieldlistmappingobjects is not None):
        for entry in Fieldlistmappingobjects:
            if (str(entry) not in ['telefon', 'telefax', 'email']):
                liste.append(entry.fieldname)
    return liste






#Form for create/edit Adress
class Addressform(forms.ModelForm):

    class Meta:

        model = Clientaddress
        exclude = ["id","trash","is_deleteable","is_editable","create_date","modified_date","create_user","modified_user","delete_user",'user_rights_link','addressindividualfields','searchvriteria_address_link','Telefon_address_link','Email_address_link','Telefax_address_link','group_rights-link','change_date','owner','occurrence','searchcriteria_address_link','task_assigned_to']

        labels = {"kurzname":'Kurzname','homepage':"Homepage",'telefon':"Telefon",'telefax':"Telefax",'email':"Email",'firstname':"Vorname",'lastname':"Nachname",'birthdate':"Geburtsdatum",'company':"Firma",'country':"Land",'city':"Ort",'zip':"PLZ",'street':"Straße",'salutation':'Anrede','letter_salutation':"Briefanrede",'is_active':'Aktiv'}



    def savecommunication(self,obj,Model):
            entry = self.cleaned_data.get(Model.lower())
            splits = entry.split(',')

            model = eval(Model)

            entry = model.objects.filter(address_link=obj.pk)

            if (entry is not None):
                    entry.delete()
            object = model.objects.filter(address_link=obj, is_standard=True).first()

            if (object is not None):
                    is_standard = True
            else:
                    is_standard = False

            for split in splits:
                    if (object is not None):
                        if (object.eintrag == split):
                            continue
                    if (split.strip() == ""):
                        continue
                    if (is_standard):
                        model.objects.get_or_create(address_link=obj, eintrag=split, is_standard=False)
                    else:
                        model.objects.get_or_create(address_link=obj, eintrag=split, is_standard=True)



    def save(self, force_insert=False, force_update=False, commit=True):
        obj = super().save( commit=commit)
        # Telefon relationen eintragen
        self.savecommunication(obj,"Telefon")
        self.savecommunication(obj, "Telefax")
        self.savecommunication(obj, "Email")
        return obj

    def __init__(self, *args, **kwargs):

        instance = kwargs.get('instance', None)
        super(Addressform, self).__init__(*args, **kwargs)

        self.fields['interest_in_link'].queryset = Addressproperties.objects.filter(fieldname='interest_in')
        self.fields['properties_link'].queryset = Addressproperties.objects.filter(fieldname='properties')
        self.fields['salutation'].queryset = Addresschoices.objects.filter(fieldname='salutation')
        self.fields['title'].queryset = Addresschoices.objects.filter(fieldname='title')
        self.fields['preferred_contacttype'].queryset = Addresschoices.objects.filter(fieldname='preferred_contacttype')
        self.fields['origin_contact'].queryset = Addresschoices.objects.filter(fieldname='origin_contact')
        self.fields['dsgvo_status'].queryset = Addresschoices.objects.filter(fieldname='dsgvo_status')






        if (instance is not None):
            self.fields['telefon'] = forms.CharField(label="Telefon", initial="",
                                                     widget=textarea_urllink(url=reverse('TelefonListView_adressid',
                                                                                         kwargs={
                                                                                             'addressid': instance.id}),
                                                                             attrs={'class': 'selectize_fon', }),
                                                     required=False)
            self.fields['telefax'] = forms.CharField(label="Telefax", initial="",
                                                     widget=textarea_urllink(url=reverse('TelefaxListView_adressid',
                                                                                         kwargs={
                                                                                             'addressid': instance.id}),
                                                                             attrs={'class': 'selectize_fon', }),
                                                     required=False)
            self.fields['email'] = forms.CharField(label="Email", initial="",
                                                   widget=textarea_urllink(url=reverse('EmailListView_emailid',
                                                                                       kwargs={
                                                                                           'addressid': instance.id}),
                                                                           attrs={'class': 'selectize_email', }),
                                                   required=False)

            self.fields['telefon'].initial = listtocommaseperated(Telefon.objects.filter(address_link=instance))

            self.fields['telefax'].initial = listtocommaseperated(Telefax.objects.filter(address_link=instance))
            self.fields['email'].initial = listtocommaseperated(Email.objects.filter(address_link=instance))
        else:
            self.fields['telefon'] = forms.CharField(label="Telefon", initial="",
                                                     widget=textinputfeld(),
                                                     required=False)
            self.fields['telefax'] = forms.CharField(label="Telefax", initial="",
                                                     widget=textinputfeld(),
                                                     required=False)
            self.fields['email'] = forms.CharField(label="Email", initial="",
                                                   widget=textinputfeld(),
                                                   required=False)



class Emailform(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('address_link','eintrag','is_active','is_standard' )

        widgets = { 'address_link': selectfield,  'is_active':checkbox, 'is_standard':checkbox}

        labels = {'address_link': "Adresslink", 'eintrag': "Email Adresse", 'is_active': "Aktiv",  'is_standard': "Standardemail Adresse"}

    eintrag = forms.RegexField(regex="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", widget=textinputfeld)

class Telefonform(forms.ModelForm):
            class Meta:
                model = Telefon
                fields = ('address_link', 'eintrag', 'is_active', 'is_standard')

                widgets = {'address_link': selectfield, 'is_active': checkbox,
                           'is_standard': checkbox}

                labels = {'address_link': "Adresslink", 'eintrag': "Telefonnummer", 'is_active': "Aktiv",
                          'is_standard': "Standard-Telefonnummer"}

            eintrag = forms.RegexField(regex = "^([+](\d{1,3})\s?)?((\(\d{3,5}\)|\d{3,5})(\s)?)\d{3,8}$", widget=textinputfeld)


class Telefaxform(forms.ModelForm):
    class Meta:
        model = Telefax
        fields = ('address_link', 'eintrag', 'is_active', 'is_standard')

        widgets = {'address_link': selectfield, 'is_active': checkbox,
                   'is_standard': checkbox}

        labels = {'address_link': "Adresslink", 'eintrag': "Telefaxnummer", 'is_active': "Aktiv",
                  'is_standard': "Standard-Telefaxnummer"}

    eintrag = forms.RegexField(regex="^([+](\d{1,3})\s?)?((\(\d{3,5}\)|\d{3,5})(\s)?)\d{3,8}$", widget=textinputfeld)