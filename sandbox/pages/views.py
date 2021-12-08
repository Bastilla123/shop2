from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView
#from settings.models import UserSettings
from photo.models import Photo
from globalsettings.models import UserSettings

# Create your views here.

# Create your views here.

def impressumview(request):
    return render(request,'pages/impressum.html')

def gobdview(request):
    return render(request,'pages/gobd.html')

def revisionssicherheitview(request):
    return render(request,'pages/revisionssicherheit.html')


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['photos'] = Photo.objects.exclude(user_link__isnull=True)
        return context



