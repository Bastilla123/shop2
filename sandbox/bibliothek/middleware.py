from testimonials.models import Testimonialmodel
from globalsettings.models import Globalsettings
import threading
#from clientaddress.forms import Newsletterform
from django import forms
from clientaddress.models import Clientaddress
from bibliothek.Widgets import *
from photo.models import Photo
from django.conf import settings

def show_tax_separately(request):
    show_tax_separately \
        = getattr(settings, 'OSCAR_SHOW_TAX_SEPARATELY', False)

    return {'show_tax_separately': show_tax_separately}

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
    fields = ["salutation","firstname","lastname",]
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

    self.fields['text'] = forms.CharField(label="Text *", initial="",
                                           widget=textarea(),
                                           required=False)



def NewsletterMiddleware(request):
  context = {}
  context["newsletter"] = Newsletterform()
  context["kontakt"] = Kontaktform()

  context["globalsettings"] = Globalsettings.objects.first()

  context["testimonials"] = Testimonialmodel.objects.order_by('-create_date')[0:4]
  # Logo
  photo = Photo.objects.filter(imagetype=0).first()
  if (photo is not None):
      # context['logo'] = photo.file
      context['logo'] = photo
  return context


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


def force_default_language_middleware(get_response):
    """
        Ignore Accept-Language HTTP headers

        This will force the I18N machinery to always choose settings.LANGUAGE_CODE
        as the default initial language, unless another one is set via sessions or cookies

        Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
        namely django.middleware.locale.LocaleMiddleware
        """
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            request.META['HTTP_ACCEPT_LANGUAGE'] = 'de'

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware



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