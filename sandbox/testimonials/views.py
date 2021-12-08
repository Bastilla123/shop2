from django.shortcuts import render
from .models import Testimonialmodel
from photo.forms import PhotoForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import (


    UpdateView,
CreateView,
)
from .forms import Testimonialform
from django.urls import reverse_lazy
from django.views.generic import ListView
from multi_form_view import MultiFormView,MultiModelFormView
# Create your views here.


@method_decorator(login_required, name='dispatch')
class TestimonialsUpdateView(UpdateView):
    template_name = "testimonials/form.html"
    model = Testimonialmodel
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    form_class = Testimonialform
    success_url = reverse_lazy('globalsettings:Test')

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
            obj = Testimonialmodel().save()

        return obj




    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['photoform'] = PhotoForm()
        return context

