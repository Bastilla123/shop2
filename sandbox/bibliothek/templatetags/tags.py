
from catalogue.models import sizechoices,colorchoices,materialchoices,brandchoices
from django import template
register = template.Library()
from photo.models import Photo
from catalogue.models import Tax

@register.filter
def get_type(value):
    return str(type(value))

@register.filter
def substract(originalvalue,substractvalue):
    return originalvalue-substractvalue

@register.filter
def getform(forms, key):
    print("Drin "+str(key))
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


@register.filter(name='getvaluefromfield')
def getvaluefromfield(dictionary,fieldname):

    fieldname = fieldname.replace('"','')

    fieldname = fieldname.strip()
    if (fieldname.strip() == ""):
        return
    try:
        fieldtype = eval(dictionary._meta.object_name)._meta.get_field(fieldname).get_internal_type()
    except Exception as e:
        print("Exception "+str(e))
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



@register.filter(name='getlogo')
def getlogo():
    logo = Photo.objects.filter(imagetype=1).first()
    if (logo is not None):
        return logo.file
    return
