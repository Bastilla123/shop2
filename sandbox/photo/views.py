from globalsettings.models import Globalsettings
from django.urls import reverse

from .forms import *

from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect,  JsonResponse
from PIL import Image, ImageOps
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

@login_required
def deletephoto(request, id):
    Attachmenteintrag = Photo.objects.filter(id=id).first()

    if (Attachmenteintrag is None):
        return HttpResponseRedirect(reverse('GlobalsettingsUpdateView'))

    BASEMedia_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASEMedia_DIR += settings.MEDIA_URL
   
    if (os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(Attachmenteintrag.file)))):
        os.remove(os.path.join(settings.MEDIA_ROOT, str(Attachmenteintrag.file)))
    
    Attachmenteintrag.delete()
    return HttpResponseRedirect(reverse('GlobalsettingsUpdateView'))


def photo_list(request,imagetype):
    photos = Photo.objects.all()
    if request.method == 'POST':

        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():

            # Da es nur ein Photo geben darf das alte löschen
            try:
                if (imagetype == 0):
                    photoentry = Photo.objects.filter(user_link=request.user).first()
                if (imagetype == 1):
                    photoentry = Photo.objects.filter(globalsettings_link=Globalsettings.objects.first()).first()
            except Exception as e:
                messages.error(request, "Es konnte das Bild nicht gefunden werden: " + str(e))
                return HttpResponseRedirect('/')
            if (photoentry is not None):

                photoentry.delete()

            post = form.save()
            post.imagetype = imagetype
            if (imagetype == 0):
                post.user_link = request.user
            if (imagetype == 1):
                post.globalsettings_link = Globalsettings.objects.first()
            try:
                post.save()
            except Exception as e:

                messages.error(request, "Beim Speichern des Bildes #1 ist folgender Fehler aufgetreten: " + str(e))
                return HttpResponseRedirect('/')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print("Not valid")
    else:
        form = PhotoForm()
        if (imagetype == 0):
            photos = Photo.objects.filter(user_link=request.user.id)

        if (imagetype == 1):
            photos = Photo.objects.filter(globalsettings_link=Globalsettings.objects.first())
    return render(request, 'photo/basisphotoform.html', {'forms':{'PhotoForm': form}, 'photos': photos})

def uploadphoto(request,imagetype): #type 0 = userphoto 1 = mandatelogo

    if request.method == 'POST':
        print("Post")
        if (not (request.user.is_authenticated)):
            messages.error(request,
                           'Diese Funktion ist nur eingeloggten Usern möglich. Bitte zuerst <a href="/signup/">registrieren</a>/<a href="/login/">einloggen</a>')
            form = PhotoForm(request.POST, request.FILES)
            return render(request, 'homepage/uploadform.html',
                          {'form': form, })

        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():


            #Da es nur ein Photo geben darf das alte löschen
            try:
                if (imagetype == 0):
                    photoentry = Photo.objects.filter(user_link=request.user).first()
                if (imagetype == 1):
                    photoentry = Photo.objects.filter(globalsettings_link=Globalsettings.objects.first()).first()
            except Exception as e:
                messages.error(request, "Beim Löschen des Bildes ist folgender Fehler aufgetreten: "+str(e))
                return HttpResponseRedirect('/')
            if (photoentry is not None):
                photoentry.delete()

            post = form.save()
            post.imagetype = imagetype
            if (imagetype == 0):

                post.user_link = request.user
            if (imagetype == 1):

                post.globalsettings_link = Globalsettings.objects.first()
            try:
                post.save()
            except Exception as e:
                messages.error(request, "Beim Speichern des Bildes #1 ist folgender Fehler aufgetreten: "+str(e))
                return HttpResponseRedirect('/')


            #Kopieren des Thumbnails in eine neue Datei und diese auch in der Datenbank verlinken danach nach Thumbnail verkleinern
            name, extension = os.path.splitext(str(post.thumbnail))
            filename = os.path.join(settings.MEDIA_ROOT, str(name))


            try:
                os.popen('cp '+str(filename)+str(extension)+' '+str(filename)+'_full'+str(extension))
            except Exception as e:
                messages.error(request, "Beim kopieren des Files: "+str(filename)+str(extension)+" Nach: "+str(filename)+str(extension)+'_full'+" trat ein Fehler auf: "+str(e))

            post.photo = str(name)+'_full'+str(extension)
            post.save()

            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')

            image = Image.open(post.thumbnail)
            cropped_image = image.crop((x, y, w + x, h + y))

            try:
                cropped_image.save(post.thumbnail.path)
            except Exception as e:
                messages.error(request, "Beim Speichern des Bildes #2 ist folgender Fehler aufgetreten: "+str(e))

            if (imagetype == 0):
                return HttpResponseRedirect(reverse('uploadphoto', kwargs={'imagetype': 0}))
            else:
                return HttpResponseRedirect(reverse('GlobalsettingsUpdateView', kwargs={'pk': 1}))
    else:
        form = PhotoForm()
        if (not (request.user.is_authenticated)):
            messages.error(request,
                           'Diese Funktion ist nur eingeloggten Usern möglich. Bitte zuerst <a href="/signup/">registrieren</a>/<a href="/login/">einloggen</a>')
            return render(request, 'homepage/uploadform.html',
                          {'form': form, 'title': "Suchetanzpartner: Hochladen von Bildern",
                           'description': "Zu dem Benutzerprofil weitere Bilder hochgeladen und ein einzelnes als Hauptfoto deklariert werden",
                           'canonical': "https://suchetanzpartner.de/uploadfile/", })

        else:
            if (imagetype==0):
                attachmentlist = Photo.objects.filter(user_link=request.user.id)

            if (imagetype==1):

                attachmentlist = Photo.objects.filter(globalsettings_link = Globalsettings.objects.first())

            print("Drin")

            
            return render(request, 'photo/basisphotoform.html',
                          {'PhotoForm': form,'type':type, 'attachmentlist': attachmentlist,
                           })
