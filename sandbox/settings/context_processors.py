from settings.models import Globalsettings
from photo.models import Photo


from django.urls import reverse


def globaldicts(request):


        context = {}

        #Impressum
        context['globalsettings'] = Globalsettings.objects.first()



        #Logo
        photo = Photo.objects.filter(imagetype=1).first()
        if (photo is not None):
            #context['logo'] = photo.file
            context['logo'] = photo



        return context

