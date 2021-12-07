from globalsettings.models import Globalsettings
import threading
#from clientaddress.forms import Newsletterform
from django import forms
from clientaddress.models import Clientaddress
from bibliothek.Widgets import *
from photo.models import Photo

class Newsletterform(forms.ModelForm):
  class Meta:
    model = Clientaddress
    fields = ["interest_in_link","salutation","title","firstname","lastname","street","zip","city"]
    widgets = {"interest_in_link":multiselectfield,"salutation":selectfield,'title': textinputfeld, 'firstname': textinputfeld, 'lastname': textinputfeld, 'street': textinputfeld, 'zip': integerfeld, 'city': textinputfeld}
  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    self.fields['telefon'] = forms.CharField(label="Telefon", initial="",
                                             widget=textinputfeld(),
                                             required=False)
    self.fields['email'] = forms.CharField(label="E-Mail *", initial="",
                                             widget=textinputfeld(),
                                             required=False)

class Kontaktform(forms.ModelForm):
  class Meta:
    model = Clientaddress
    fields = ["salutation","title","firstname","lastname","street","zip","city"]
    widgets = {"salutation":selectfield,'title': textinputfeld, 'firstname': textinputfeld, 'lastname': textinputfeld, 'street': textinputfeld,
               'zip': integerfeld, 'city': textinputfeld}
  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    self.fields['telefon'] = forms.CharField(label="Telefon", initial="",
                                             widget=textinputfeld(),
                                             required=False)
    self.fields['email'] = forms.CharField(label="E-Mail *", initial="",
                                             widget=textinputfeld(),
                                             required=False)
    self.fields['subject'] = forms.CharField(label="Subject *", initial="",
                                           widget=textinputfeld(),
                                           required=False)
    self.fields['text'] = forms.CharField(label="Text *", initial="",
                                           widget=textarea(),
                                           required=False)



def NewsletterMiddleware(request):
  context = {}
  context["newsletter"] = Newsletterform()
  context["kontakt"] = Kontaktform()

  context["globalsettings"] = Globalsettings.objects.first()
  # Logo
  photo = Photo.objects.filter(imagetype=0).first()
  if (photo is not None):
      # context['logo'] = photo.file
      context['logo'] = photo
  return context



class RequestMiddleware:

  def __init__(self, get_response, thread_local=threading.local()):
    self.get_response = get_response
    self.thread_local = thread_local
    # One-time configuration and initialization.

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
    self.thread_local.current_request = request

    response = self.get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response