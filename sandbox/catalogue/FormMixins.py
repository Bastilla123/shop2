from PIL import Image
from django import forms
from django.contrib.auth.models import User
from .Widgets import *

from .middleware import RequestMiddleware
from django.contrib import messages


class StandardMixin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Self " + str(dir(self)))
        print("Neu " + str(self.base_fields))
        for field in self:
            print("Field " + str(field))
        fieldlist = self.Meta.model._meta.get_fields()
        excludelist = self.Meta.exclude

        for field in excludelist:
            if (field in self.fields):
                self.fields.pop(field)

        print("Charfield " + str(list(set(fieldlist) - set(excludelist))))
        for field in list(set(fieldlist) - set(excludelist)):
            # for field in self:

            try:

                self.Meta.model._meta.get_field(field)
            except Exception as e:
                print("Exception e " + str(e))
                continue

            if (field not in self.fields):
                continue

            # print("Field " + str(field) + " Type: "+str(self.Meta.model._meta.get_field(field).get_internal_type()))
            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "ManyToManyField"):

                if (hasattr(self.Meta.model._meta.get_field(field).related_model().__class__, '_mptt_meta')):

                    self.fields[field].widget = TreeCheckboxSelectMultiple(modelrelatedclass=str(str(type(
                        self.Meta.model._meta.get_field(field).related_model())).split(".")[2].replace("'>", "")))
                else:

                    self.fields[field].widget = multiselectfield()

                if ('choices' in str(type(self.Meta.model._meta.get_field(field).related_model())) or 'Choices' in str(
                        type(self.Meta.model._meta.get_field(field).related_model()))):

                    self.fields[field].queryset = eval(
                        str(self.Meta.model._meta.object_name) + 'choices').objects.filter(fieldname=field)
                else:

                    self.fields[field].choices = self.Meta.model._meta.get_field(field).get_choices()

                continue

            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "ForeignKey"):
                # print("Field " + str(field) + " Choices " + str(self.Meta.model._meta.get_field(field).get_choices()))

                if (str(type(
                        self.Meta.model._meta.get_field(field).related_model())) == "<class 'address.models.Address'>"):
                    self.fields[field].widget = selectfilterwidget(exclude=excludelist,
                                                                   model=self.Meta.model._meta.object_name)
                    continue
                try:

                    self.fields[field].widget = selectfield(
                        choices=self.Meta.model._meta.get_field(field).get_choices())
                except Exception as e:
                    self.fields[field].widget = selectfield()
                if ('choices' in str(type(self.Meta.model._meta.get_field(field).related_model()))):

                    self.fields[field].queryset = eval(
                        str(self.Meta.model._meta.object_name) + 'choices').objects.filter(fieldname=field)
                else:
                    try:
                        self.fields[field].choices = self.Meta.model._meta.get_field(field).get_choices()
                    except Exception as e:
                        pass
                continue

            if (hasattr(self.Meta.model._meta.get_field(field), 'choices')):

                if (self.Meta.model._meta.get_field(field).choices is not None):
                    self.fields[field].widget = selectfield(choices=self.Meta.model._meta.get_field(field).choices)
                    continue

            if ((str(self.Meta.model._meta.get_field(field).get_internal_type()) == "PositiveSmallIntegerField" or str(
                    self.Meta.model._meta.get_field(
                        field).get_internal_type()) == "PositiveIntegerField") and self.Meta.model._meta.get_field(
                field).choices is None):
                if (hasattr(self.Meta.model._meta.get_field(field), 'choices')):

                    if (self.Meta.model._meta.get_field(field).choices is not None):
                        self.fields[field].widget = selectfield(choices=self.Meta.model._meta.get_field(field).choices)
                        continue
                self.fields[field].widget = integerfeld()
                continue

            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "CharField"):
                self.fields[field].widget = textinputfeld()
                continue
            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "DateField"):
                self.fields[field].widget = datepickerfield()
                continue

            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "DecimalField"):
                self.fields[field].widget = decimalfeld()
                continue
            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "BooleanField"):
                self.fields[field].widget = checkbox()
                continue

            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "DateTimeField"):
                self.fields[field].widget = datetimepickerfield()
            if (str(self.Meta.model._meta.get_field(field).get_internal_type()) == "TextField"):
                self.fields[field].widget = textinputfeld()

        if (not 'instance' in kwargs):
            return
        if (kwargs['instance'] is None):
            return

        self.fields['activeTabname'] = forms.CharField(widget=forms.HiddenInput(),
                                                       required=False)  # Hiddenfield to store active tab name


