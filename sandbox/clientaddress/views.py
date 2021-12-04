from bibliothek.middleware import Newsletterform,Kontaktform
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.messages.views import SuccessMessageMixin
from bibliothek.Mixins import ListviewMixin,Deletesuccessmixin,SingleFormMixin

from django.urls import reverse, reverse_lazy
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)

from django_filters.views import FilterView

#from .filters import *

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *

from datetime import *


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#from dynamic_preferences.registries import global_preferences_registry
# We instantiate a manager for our global preferences
#global_preferences = global_preferences_registry.manager()

def submitcontactform(request):
    if request.method == 'POST':

        form = Kontaktform(request.POST)
        if form.is_valid():
            adresse = form.save(commit=True)

            # Save E-Mail
            email = form.cleaned_data["email"]
            if (email is not None):
                Email(address_link=adresse, eintrag=email, is_standard=True).save()
            # Save Telefon
            telefon = form.cleaned_data["telefon"]
            if (email is not None):
                Telefon(address_link=adresse, eintrag=email, is_standard=True).save()
            print("Cleaned "+str(form.cleaned_data))
            # send a confirmation mail
            subject = 'Neue Kontaktanfrage von Webseite mit dem Subject: '+str(form.cleaned_data[
                "subject"])
            message = 'Hallo,  Es ist eine neue Anfrage angekommen mit dem Text: '+str(form.cleaned_data[
                "text"])+' von der Adresse mit der Id: '+str(adresse.id)

            email_from = settings.EMAIL_HOST_USER

            recipient_list = ['sebastian.jung2@gmail.com', ]
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                response = JsonResponse({"msg": "Es konnte keine E-Mail verschickt werden. Error: " + str(e)})
                response.status_code = 403  # To announce that the user isn't allowed to publish
                return response
            res = JsonResponse({
                                   'msg': 'Danke. Wir haben Ihre E-Mail empfangen und bearbeiten diese so schnell wie möglich.'})
            return res
        else:
            response = JsonResponse({"msg": "Form ist nicht valide. Error: " + str(form.errors(escape_html=False))})
            response.status_code = 403  # To announce that the user isn't allowed to publish
            return response

    return render(request, 'index.html')

def submitnewsletter(request):
    if request.method == 'POST':

        form = Newsletterform(request.POST)
        if form.is_valid():
            adresse = form.save(commit=True)

            #Save E-Mail
            email = form.cleaned_data["email"]
            if (email is not None):
                Email(address_link=adresse,eintrag=email,is_standard=True).save()
            #Save Telefon
            telefon = form.cleaned_data["telefon"]
            if (email is not None):
                Telefon(address_link=adresse, eintrag=email, is_standard=True).save()

            # send a confirmation mail
            subject = 'Bestätigung NewsLetter'
            message = 'Hallo ' + form.cleaned_data["lastname"] + ', Danke für das Interesse an unserem Newsletter. Sie bekommen zukünftig regelmäßig die neuesten News von uns. '

            email_from = settings.EMAIL_HOST_USER

            recipient_list = [email, ]
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                response = JsonResponse({"msg": "Es konnte keine E-Mail verschickt werden. Error: " + str(e)})
                response.status_code = 403  # To announce that the user isn't allowed to publish
                return response
            res = JsonResponse({'msg': 'Danke. Wir haben Ihnen eine E-Mail zugeschickt. Um den Newsletter zu bestätigen klicken Sie den Link in der E-Mail'})
            return res
        else:
            response = JsonResponse({"msg": "Form ist nicht valide. Error: "+str(form.errors(escape_html=False))})
            response.status_code = 403  # To announce that the user isn't allowed to publish
            return response



    return render(request, 'index.html')

def validate_email(request):
    email = request.POST.get("email", None)
    from .models import Email
    import re
    if email is None:
        res = JsonResponse({'msg': 'Emailadresse ist zwingend nötig.'})
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Ungültige E-Mail Adresse'})
    elif Email.objects.filter(eintrag = email).exists():
        response = JsonResponse({"msg": "Es gibt bereits ein Adressdatensatz mit dieser E-Mail Adresse"})
        response.status_code = 403  # To announce that the user isn't allowed to publish
        return response


    else:
        res = JsonResponse({'msg': ''})
    return res

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
class AddressCreateView(SingleFormMixin,CreateView):
    model = Clientaddress

    form_class = Addressform
    success_url = reverse_lazy('addresslist')



    def form_invalid(self, form):

        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required, name='dispatch')
class AddressUpdateView(SingleFormMixin,UpdateView):
    model = Clientaddress
    form_class = Addressform
    success_url = reverse_lazy('addresslist')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
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

    return render(request, 'marketing/message.html')

@method_decorator(login_required, name='dispatch')
class AddressListView(ListviewMixin, FilterView):
    model = Clientaddress

    buttons = {0:{'url':reverse_lazy('AddressCreateView'),'awesomefont':"fas fa-plus",'label':'Neue Adresse anlegen'}}


@method_decorator(login_required, name='dispatch')
class DeleteAddressView(Deletesuccessmixin,DeleteView):
    model=Clientaddress


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


    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Email Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('AddressEmailCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Email anlegen'}}


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Clientaddress.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Email.objects.filter(address_link=Adressentry)
        return data


@method_decorator(login_required, name='dispatch')
class EmailDeleteView(Deletesuccessmixin, DeleteView):
    model = Email
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


    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Telefon Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('TelefonCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Telefonnummer anlegen'}}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Clientaddress.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Telefon.objects.filter(address_link=Adressentry)
        return data





@method_decorator(login_required, name='dispatch')
class TelefonDeleteView(Deletesuccessmixin, DeleteView):
    model = Telefon
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


    fieldlist = ('id','address_link','eintrag','is_active','is_standard' )
    labels = {'id': 'Id', 'address_link': 'Addresse', 'eintrag': 'Telefax Adresse', 'is_active': 'Aktiv', 'is_standard': 'Standard'}
    buttons = {0: {'url': reverse_lazy('TelefaxCreateView'), 'awesomefont': "fas fa-plus",
                   'label': 'Neue Telefaxnummer anlegen'}}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if ('addressid' in self.kwargs):

            Adressentry = Clientaddress.objects.filter(id=self.kwargs['addressid']).first()
            if (Adressentry):
                data['object_list'] = Telefax.objects.filter(address_link=Adressentry)
        return data



@method_decorator(login_required, name='dispatch')
class TelefaxDeleteView(Deletesuccessmixin, DeleteView):
    model = Telefax


    success_url = reverse_lazy('TelefaxListView')




