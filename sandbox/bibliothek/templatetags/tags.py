from clientaddress.models import Clientaddress
from django.contrib.auth.models import User

from django import template
register = template.Library()


@register.filter
def get_type(value):
    return str(type(value))

@register.filter
def substract(originalvalue,substractvalue):
    return originalvalue-substractvalue

@register.filter
def getform(forms, key):

    if (key in forms):


        return forms[key]
    return ""


@register.filter(name='getmanytomanyvalues')
def getmanytomanyvalues(instance,fieldname):

    attr = getattr(instance,str(fieldname)).all()

    if ('None' in attr):
        return ""
    string = ""
    i = 0
    for items in attr:
        if (i != 0):
            string +=','
        string += str(items)
        i += 1


    return string


@register.filter
def get_attr(value, arg):

    try:
        if (value._meta.get_field(arg).choices is not None):
            for choice_entry in value._meta.get_field(arg).choices:

                if (choice_entry[0] == getattr(value,arg)):
                    return choice_entry[1]
    except Exception as e:

        return getattr(value, arg)


    try:
        value = getattr(value, arg)

        if (value is None):
            return ""
        return value
    except:
        return ""
    return ""

@register.filter(name='desctimes')
def desctimes(number,descnumber):
    if (number is None):
        return None
    number += 1
    return range(1,int(number)-int(descnumber))

@register.filter(name='times')
def times(number):
    if (number is None):
        return None
    number += 1
    return range(1,int(number))

@register.filter(name='getvaluefromfield')
def getvaluefromfield(dictionary,fieldname):

    fieldname = fieldname.replace('"','')

    fieldname = fieldname.strip()
    if (fieldname.strip() == ""):
        return
    try:
        fieldtype = eval(dictionary._meta.object_name)._meta.get_field(fieldname).get_internal_type()
        #print("Fieldname "+str(fieldname)+" Internal Type "+str(fieldtype))
    except Exception as e:
        print("Eval funktioniert nicht von dictionary._meta.object_name")
        return ""

    if (fieldtype == "DateTimeField"):

        feldeintrag = get_attr(dictionary, fieldname)


        if (str(type(feldeintrag)) == "<class 'datetime.datetime'>"):
            return get_attr(dictionary, fieldname).strftime("%d.%m.%Y %H:%m")
        return get_attr(dictionary, fieldname)
    elif (fieldtype == "ManyToManyField"):

        return getmanytomanyvalues(dictionary,fieldname)
    elif (fieldtype == "BooleanField"):

        if (get_attr(dictionary, fieldname) == True):
            return '<i class="fas fa-check"></i>'
        else:
            return '<i class="fa fa-times" aria-hidden="true"></i>'
    elif (fieldtype == "OneToOneField"):

        return ""

    return get_attr(dictionary, fieldname)

@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)


#from random import randint
#@register.simple_tag
#def random_number(forms):
#    return randint(0,999)


@register.filter(name='getcheckboxes')
def getcheckboxes(allfieldlist,activefieldlist):

    deletelist = ['is_deleteable','is_editable','trash','create_date','is_active','modified_date','create_user','modified_user','delete_user','change_date']
    html = '<div class="custom-control ">'

    for field in allfieldlist:
        if (field in deletelist):
            continue
        html += '<div class="form-group"><label for="id_homepage">'+str(translateheader(field))+':</label><div class="form-group">'
        found = False

        for activefield in activefieldlist:

            if (field.strip()==activefield.strip().replace('"','')):

                found = True

                html += '<input type="checkbox" name="id_'+str(field)+'" id="id_'+str(field)+'" style="border-radius: 4px;" checked="">'
                break
        if (found==False):
            html += '<input type="checkbox" name="id_'+str(field)+'" id="id_'+str(field)+'" style="border-radius: 4px;" >'


        html += '</div></div>'



    return html


@register.filter(name='getlinkfromfield')
def getlinkfromfield(instance,fieldname):
    attr = get_attr(instance, fieldname)
    model = attr._meta.model_name
    return '<a href="/edit/' + str(model) + "/" + str(attr.id) + '">' + str(attr) + "</a>"

@register.filter(name='times')
def times(number):
    if (number is None):
        return None
    number += 1
    return range(1,int(number))

@register.filter(name='getallfieldsfrommodel')
def getallfieldsfrommodel(modelname):

    model = eval('Clientaddress')
    allfields = [f.name for f in model._meta.get_fields()]


    return allfields


@register.filter(name='translateheader')
def translateheader(fieldname):
    fieldname = fieldname.replace('"','').replace(' ','')

    translatedict = {'kurzname': 'Kurzname', 'firstname': 'Vorname', 'lastname': 'Nachname', 'city': 'Ort', 'id': 'Id','zip':'PLZ','letter_salutation':'Briefanrede','birthdate':'Geburtstag',
              'is_active': 'Aktiv', 'country': 'Land',"status":"Status","title":'Überschrift','description':"Beschreibung",'date':"Datum",'assigned_to':"Zugordneter Benutzer",'queue_link':"Zugeordnete Queue",'address_link':"Zugeordnete Adresse","priority":"Priorität"
              }
    for key,value in translatedict.items():

        if (key==fieldname):


                    return value



    return fieldname