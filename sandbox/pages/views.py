from catalogue.models import Category,ProductCategory,Product
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView
#from settings.models import UserSettings
from photo.models import Photo
from globalsettings.models import UserSettings,Globalsettings
from .forms import Widerrufform
from globalsettings.models import Globalsettings
from bibliothek.Widgets import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

# Create your views here.

def revocation(request):

    if request.method == 'POST':

        form = Widerrufform(request.POST)
        if form.is_valid():








            email = form.cleaned_data['email']
            from django.template.loader import render_to_string
            product= form.cleaned_data['product']
            context = {'product':product}


            message = render_to_string('pages/widerrufemail_customer.html',context)
            try:
                msg = EmailMessage('Bestätigung Widerruf', message, settings.EMAIL_HOST_USER, [email])
                msg.content_subtype = 'html'
                msg.send()
            except Exceptions as e:
                print("Expetion "+str(e))

            context = {'salutation': form.cleaned_data['salutation'], 'firstname': form.cleaned_data['firstname'],
                                        'lastname': form.cleaned_data['lastname'], 'companyname':form.cleaned_data['companyname'],'street':form.cleaned_data['street']
                                        ,'zip':form.cleaned_data['zip'],'city':form.cleaned_data['city'],'order_date':form.cleaned_data['order_date'],'email':email,
                                        'product':product
                                        }
            message = render_to_string('pages/widerrufemail_shop.html', context)
            globalsettingsentry = Globalsettings.objects.first()

            try:
                msg = EmailMessage('Widerruf eingegangen von Shop', message, settings.EMAIL_HOST_USER, [globalsettingsentry.email])
                msg.content_subtype = 'html'
                msg.send()
            except Exceptions as e:
                print("Expetion " + str(e))
            messages.info(request, 'Der Widerruf ist erfolgreich eingegangen. Wir haben ihnen eine Bestätigungs E-Mail geschickt')

    form = Widerrufform()

    return render(request,'pages/widerruf.html',{'form':form,'globalsettings':Globalsettings.objects.first()})


def ecodms(request):

    category = Category.objects.filter(name = 'EcoDMS')
    productcategorie = ProductCategory.objects.filter(category__in = category)
    return render(request,'pages/ecodms.html',{'productcategorie':productcategorie})

def impressumview(request):
    return render(request,'pages/impressum.html')

def about_us(request):
    return render(request,'pages/about_us.html')

def gobdview(request):
    return render(request,'pages/gobd.html')

def revisionssicherheitview(request):
    return render(request,'pages/revisionssicherheit.html')

def csr(request):
    return render(request,'pages/csr.html')

def payment(request):
    return render(request,'pages/payment.html')
def behavior_rules(request):
    return render(request,'pages/behavior_rules.html')
def datamigration(request):
    return render(request,'pages/datamigration.html')
def contact(request):
    return render(request,'pages/contact.html')
def agb(request):
    return render(request,'pages/agb.html')
def privacy_statement(request):
    return render(request,'pages/privacy_statement.html')
def contact_us(request):
    context = {}
    context['globalsettings'] = Globalsettings.objects.first()
    return render(request,'pages/contact_us.html',context)




class Teamlistview(ListView):
    model = UserSettings
    template_name = 'pages/team.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['photos'] = Photo.objects.exclude(user_link__isnull=True)
        return context





class Teamlistview(ListView):
    model = UserSettings
    template_name = 'pages/team.html'




