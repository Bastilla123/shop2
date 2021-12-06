from photo.models import Photo
from photo.forms import PhotoForm

from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.generic.edit import (


    UpdateView,
CreateView,
)
from django.views.generic import ListView
from django.urls import reverse_lazy
from .filter import *
from django.utils.decorators import method_decorator
from multi_form_view import MultiFormView,MultiModelFormView
from django_filters.views import FilterView
from bibliothek.Mixins import ListviewMixin





@method_decorator(login_required, name='dispatch')
class UserCreateView(MultiModelFormView,CreateView):
    model = User
    template_name = 'pages/userprofile.html'
    success_message = 'Datensatz wurde erfolgreich angelegt'
    form_classes = {
        'basisdata': Userform,
        'Userextendform': Userextendform,

    }
    success_url = reverse_lazy('Userlistview')


    def forms_valid(self, forms):
        userentry = forms['basisdata'].save()
        record = forms['Userbasistemplate'].save(commit=False)
        record.user_link = self.request.user
        record.save()
        return super(UserCreateView, self).forms_valid(forms)

@method_decorator(login_required, name='dispatch')
class Userlistview(ListviewMixin,ListView):
    model = User
    template_name = 'liststandardtemplate.html'
    fieldlist = ('id','username', 'first_name', 'last_name', 'email' )

    buttons = {
        0: {'url': reverse_lazy('globalsettings:Userlistview'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},
        1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print("Context "+str(context))
        return context



@method_decorator(login_required, name='dispatch')
class UserUpdateView(MultiModelFormView,UpdateView):
    model = User
    template_name =  'settings/globalsettings.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    form_classes = {
        'basisdata': Userform,
        'Userextendform': Userextendform,
    }
    success_url = reverse_lazy('Userlistview')
    user_id = None


    def get_success_url(self):
        return reverse_lazy('Userlistview')

    def get_objects(self):
        self.user_id = self.kwargs.get('pk', None)

        return {
            'basisdata': self.request.user,

            'Userextendform': self.request.user.usersettings_user_link,

        }

    def save(self, commit=True):
        objects = super().save(commit=False)

        return objects

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if (hasattr(self.request.user,'userimage')):
            context['photos'] = self.request.user.userimage


        context['photoform'] = PhotoForm()

        return context


@method_decorator(login_required, name='dispatch')
class GlobalsettingsUpdateView(UpdateView):
    template_name = "settings/globalsettings.html"
    model = Globalsettings
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    form_class = Settingsform
    success_url = reverse_lazy('GlobalsettingsUpdateView')

    def get_object(self, queryset=None):

        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = 1
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)


        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = Globalsettings().save()

        return obj




    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['photos'] = Photo.objects.filter(globalsettings_link=Globalsettings.objects.first())

        context['photoform'] = PhotoForm()

        return context

