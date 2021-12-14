from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView
#from settings.models import UserSettings
from photo.models import Photo
from globalsettings.models import UserSettings,Globalsettings


# Create your views here.

# Create your views here.

def impressumview(request):
    return render(request,'pages/impressum.html')

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




