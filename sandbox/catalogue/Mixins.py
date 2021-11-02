#from .middleware import RequestMiddleware

from itertools import chain
from django.contrib import messages

class ListviewMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context ['buttons'] = self.buttons
        context ['fieldlist'] = self.fieldlist

        context ['model'] = str(self.model._meta.model_name)
        print("Context "+str(context))
        return context

class Deletesuccessmixin():
    def get_template_names(self):
        return "website/deletetemplate.html"
    def get_success_url(self):

        referer = self.request.POST.get('referer')
        if (referer != "" and referer is not None):
            return referer
        else:
            return '/'

class SingleFormMixin():


    @staticmethod
    def to_dict(self, instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            if instance._meta.get_field(f.name).get_internal_type() == 'ForeignKey':
                data[f.name] = instance.__getattribute__(f.name).__str__()
            else:
                data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.__str__() for i in f.value_from_object(instance)]
        data['id'] = instance.pk
        return data


    @staticmethod
    def result_function(self, fields, qs):
        result = []

        for b in qs:
            object = self.object_class.objects.get(pk=b['pk'])
            col = self.to_dict(self, object)
            result.append(col)
        return result

    def get_queryset(self):
        return self.model.objects.all()

    def set_object(self, request):
        if not resolve(request.path).url_name == 'add':
            queryset = self.get_queryset()
            self.object = self.get_object(queryset=queryset)
        else:
            self.object = None

    @staticmethod
    def find_match(self, string_list, wanted):
        for string in string_list:
            if string.startswith(wanted):
                return string
        return None




    def form_valid(self,form):
        if ('create' in self.request.get_full_path()):
            messages.success(self.request, "Der Eintrag wurde angelegt")
        if ('edit' in self.request.get_full_path()):
            messages.success(self.request, "Der Eintrag wurde erfolgreich aktualisiert")



        return super().form_valid(form)
