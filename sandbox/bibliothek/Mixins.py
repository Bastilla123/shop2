#from .middleware import RequestMiddleware

from itertools import chain
from django.contrib import messages

class ListviewMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context ['buttons'] = self.buttons

        allfields = self.model._meta.get_fields()

        allfields2 = []
        for field in allfields:

            if (str(type(field)) != "<class 'django.db.models.fields.reverse_related.ManyToOneRel'>"):
                allfields2.append(field.name)

        if hasattr(self,'exlude'):
            excludefields = self.exclude
            context['fieldlist'] = list(set(allfields2) - set(excludefields))
        else:
            context['fieldlist'] = allfields2

        #context ['fieldlist'] = self.fieldlist

        context ['model'] = str(self.model._meta.model_name)

        return context

    def get_queryset(self):

        if (self.template_name is None):


                self.template_name = 'liststandardtemplate.html'

        return super().get_queryset()

class Deletesuccessmixin():
    def get_template_names(self):
        return "deletetemplate.html"
    def get_success_url(self):
        if hasattr(self,'success_url'):
            return self.success_url
        referer = self.request.POST.get('referer')
        if (referer != "" and referer is not None):
            return referer
        else:
            return '/'

class SingleFormMixin():



    def get_context_data(self, *args, **kwargs):

        if (not hasattr(self,'template_name') or self.template_name is None):
            self.template_name =  'formstandardtemplate.html'

        data = super().get_context_data(*args, **kwargs)

        data['model'] = self.model.__name__


        return data