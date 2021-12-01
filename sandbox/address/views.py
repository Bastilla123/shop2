
from searchcriteria.models import Searchcriteria
from emailmarketing.ViewsMixins import Viewindividualfields
from django.db.models import Max
from django.contrib.messages.views import SuccessMessageMixin
from settings.models import UserSettings
from settings.models import Tabs,IndividualFields,Box
from django.http import HttpResponse
from settings.models import Globalsettings
from emailmarketing.Mixins import ListviewMixin,Deletesuccessmixin,SingleFormMixin
from emailmarketing.RightsMixins import ListRightsModel,DeleteRightsModel,UpdateRightsModel
from historie.helpers import newHistorie_create_update
from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    ModelFormMixin,
    ProcessFormView,
    UpdateView,
)
from django.views.generic import ListView
from django_filters.views import FilterView
from django.shortcuts import render
from .forms import *
from .filters import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.http.response import HttpResponseRedirect,  JsonResponse
from django.utils.encoding import force_bytes, force_text

from django.shortcuts import render, redirect
from .forms import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from datetime import *
from django.utils import timezone
from django.template import Template, Context

from django.db.models import Q
from historie.models import Historie,Historietype,Historiesubtype
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from searchcriteria.views import immomatchingaddress

#from dynamic_preferences.registries import global_preferences_registry
# We instantiate a manager for our global preferences
#global_preferences = global_preferences_registry.manager()

def test(request):
    return render(request,'test2.html')


# gibt die errors aus einer Form zurück als HTML Quellcode
def gethtmlerrortext(form):
    errortext = ""
    errortext += '<ul class="errorlist">'
    for field in form:
        if field.errors:
            errortext += field.label + ': '

            for error in field.errors:
                errortext += error + '</br>'

    errortext += "</ul>"
    return errortext




def savecommunication(form,Model,post):
            entry = form.cleaned_data.get(Model.lower())
            import django
            model = django.apps.apps.get_model('address', Model)
            splits = entry.split(',')
            # delete all Model relations
            entry = model.objects.filter(address_link=post).exclude(eintrag__in=splits)

            if (entry is not None):
                    entry.delete()
            object = model.objects.filter(address_link=post, is_standard=True).first()

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
                        model.objects.get_or_create(address_link=post, eintrag=split, is_standard=False)
                    else:
                        model.objects.get_or_create(address_link=post, eintrag=split, is_standard=True)


@method_decorator(login_required, name='dispatch')
class AddressCreateView2(SingleFormMixin,CreateView):
    model = Address

    form_class = Addressform
    success_url = reverse_lazy('addresslist')

    def form_invalid(self, form):
        print("Form "+str(form))
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class AddressCreateView(SingleFormMixin,CreateView):
    model = Address

    form_class = Addressform
    success_url = reverse_lazy('addresslist')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """

        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)





@method_decorator(login_required, name='dispatch')
class AddressUpdateView(UpdateRightsModel,SingleFormMixin,UpdateView):
    model = Address
    form_class = Addressform

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)


        context['searchcriterialist'] = Searchcriteria.objects.filter(address_link=context['object'])
        context['searchcriteriamodel'] = Searchcriteria
        context['matchinglist'] = immomatchingaddress(context['object'])
        #print("Type "+str(context['object'])))
        #print("Context "+str(context))
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def subscriptionactivate(request, token):
    try:
        test = AuthToken.objects.get(token=token)
    except Exception as e:
        messages.error(request, 'Es konnte der Token: ' + str(token) + ' nicht gefunden werden!')
        return render(request, 'marketing/message.html')

    if (test is None):
        messages.error(request, 'Der Token konnte in der Datenbank nicht gefunden werden')
        return render(request, 'marketing/message.html')
    try:
        entry= Emailsubscription.objects.filter(name=test.email).first()

    except Exception as e:
        messages.error(request, 'Es gab den folgenden Errorcode: ' + str(e))
        return render(request, 'marketing/message.html')

    if(entry is not None):
        entry.subscription_status=2
        entry.ipadress_on_subscription=str(get_client_ip(request))
        entry.subscription_confirmdate=datetime.now()
        entry.save()
    else:
        messages.error(request, 'Die Email Adresse: ' + str(test.email) +" konnte in der Adresse Emailosubscription Tabelle nicht gefunden werden")
        return render(request, 'marketing/message.html')
    try:
        test.delete()
    except Exception as e:
        messages.error(request, 'Beim löschen es tokens ist folgender Fehler aufgetetreten: ' + str(e))
        return render(request, 'marketing/message.html')
    save_successfull(request, messages)
    Historie(is_deleteable=False,create_date = datetime.now(),modified_date= datetime.now(),modified_user = request.user,create_user =request.user,owner = request.user).save()
    return render(request, 'marketing/message.html')

@method_decorator(login_required, name='dispatch')
class AddressListView(ListRightsModel,ListviewMixin, FilterView):
    model = Address
    filterset_class = AddressFilter
    buttons = {0:{'url':reverse_lazy('AddressCreateView'),'awesomefont':"fas fa-plus",'label':'Neue Adresse anlegen'}}

@method_decorator(login_required, name='dispatch')
class DeleteAddressView(Deletesuccessmixin,DeleteView):
    model=Address
    template_name = "marketing/deletetemplate.html"

    success_url = reverse_lazy('addresslist')



# Email CRUD
@method_decorator(login_required, name='dispatch')
class EmailUpdateView(SingleFormMixin,UpdateView):
    model = Email

    form_class = Emailform
    success_url = reverse_lazy('EmailListView')



    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class EmailCreateView(SingleFormMixin,CreateView):
    model = Email

    form_class = Emailform
    success_url = reverse_lazy('EmailListView')




    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EmailListView(SuccessMessageMixin,ListviewMixin,FilterView):
    model = Email

    filterset_class = EmailFilter
    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Email Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('AddressEmailCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Email anlegen'}}


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Address.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Email.objects.filter(address_link=Adressentry)
        return data


@method_decorator(login_required, name='dispatch')
class EmailDeleteView(Deletesuccessmixin, DeleteView):
    model = Email
    template_name = "marketing/deletestandardtemplate.html"

    success_url = reverse_lazy('EmailListView')
    
    
# Telefon CRUD
@method_decorator(login_required, name='dispatch')
class TelefonUpdateView(SingleFormMixin,UpdateView):
    model = Telefon

    form_class = Telefonform
    success_url = reverse_lazy('TelefonListView')


    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class TelefonCreateView(SingleFormMixin,UpdateView):
    model = Telefon

    form_class = Telefonform
    success_url = reverse_lazy('TelefonListView')


    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TelefonListView(SuccessMessageMixin,ListviewMixin,FilterView):
    model = Telefon

    filterset_class = TelefonFilter
    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Telefon Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('TelefonCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Telefonnummer anlegen'}}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Address.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Telefon.objects.filter(address_link=Adressentry)
        return data





@method_decorator(login_required, name='dispatch')
class TelefonDeleteView(Deletesuccessmixin, DeleteView):
    model = Telefon
    template_name = "marketing/deletestandardtemplate.html"

    success_url = reverse_lazy('TelefonListView')
    
    
# Telefax CRUD
@method_decorator(login_required, name='dispatch')
class TelefaxUpdateView(SingleFormMixin,UpdateView):
    model = Telefax

    form_class = Telefaxform
    success_url = reverse_lazy('TelefaxListView')


    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)
        return super().form_valid(form)





@method_decorator(login_required, name='dispatch')
class TelefaxCreateView(SingleFormMixin, SuccessMessageMixin, CreateView):
    model = Telefax

    form_class = Telefaxform
    success_url = reverse_lazy('TelefaxListView')
    success_message = 'Datensatz wurde erfolgreich angelegt'


    def form_valid(self, form):

        if (form.cleaned_data.get('is_standard') == True):
            object = self.model.objects.filter(address_link=form.cleaned_data.get('address_link'))
            if (object is not None):
                object.update(is_standard = False)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TelefaxListView(SuccessMessageMixin,ListviewMixin,FilterView):
    model = Telefax

    filterset_class = TelefaxFilter
    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Telefax Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('TelefaxCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Telefaxnummer anlegen'}}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Address.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Telefax.objects.filter(address_link=Adressentry)
        return data



@method_decorator(login_required, name='dispatch')
class TelefaxDeleteView(Deletesuccessmixin, DeleteView):
    model = Telefax
    template_name = "marketing/deletestandardtemplate.html"

    success_url = reverse_lazy('TelefaxListView')




