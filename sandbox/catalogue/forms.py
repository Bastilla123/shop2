from django.db.models import Max,Min

from oscar.core.loading import get_model

from bibliothek.Widgets import *
from .models import colorchoices,brandchoices,sizechoices,materialchoices
from oscar.apps.dashboard.catalogue.forms import _attr_text_field,_attr_textarea_field,_attr_integer_field,_attr_boolean_field,_attr_float_field,_attr_date_field,_attr_datetime_field,_attr_option_field,_attr_multi_option_field,_attr_entity_field,_attr_numeric_field,_attr_file_field,_attr_image_field
from oscar.apps.dashboard.catalogue.forms import ProductForm as Productformold
from bibliothek.FormMixins import *


Product = get_model('catalogue', 'Product')
Partnermodel_stockrecord = get_model('partner', 'stockrecord')

from .models import *

class Taxform(StandardMixin):
    class Meta:
        model = Tax
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink"]




class brandform(StandardMixin):
    class Meta:
        model = brandchoices
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink"]


        labels = {'name': "Name",
              }

class materialform(StandardMixin):
    class Meta:
        model = materialchoices
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink"]


        labels = {'name': "Name",
              }

class colorform(StandardMixin):
    class Meta:
        model = colorchoices
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink"]


        labels = {'name': "Name",
              }

class Sizeform(StandardMixin):
    class Meta:
        model = sizechoices
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink"]


        labels = {'name': "Name",
              }


class ProductForm(Productformold):
    FIELD_FACTORIES = {
        "text": _attr_text_field,
        "richtext": _attr_textarea_field,
        "integer": _attr_integer_field,
        "boolean": _attr_boolean_field,
        "float": _attr_float_field,
        "date": _attr_date_field,
        "datetime": _attr_datetime_field,
        "option": _attr_option_field,
        "multi_option": _attr_multi_option_field,
        "entity": _attr_entity_field,
        "numeric": _attr_numeric_field,
        "file": _attr_file_field,
        "image": _attr_image_field,
    }

    class Meta:
        model = Product
        fields = [
            'title', 'upc', 'description', 'is_public', 'is_discountable', 'structure', 'slug', 'meta_title',
            'meta_description','product_tax']
        widgets = {
            'structure': forms.HiddenInput(),
            'meta_description': forms.Textarea(attrs={'class': 'no-widget-init'})
        }


class ProductFilterForm(forms.Form):
    def __init__(self, catalogview,*args, **kwargs):
        min_price_set = catalogview.request.GET.get('price_min_range', None)

        price = Partnermodel_stockrecord.objects.aggregate(Min('price'),Max('price'))

        max_price_set = catalogview.request.GET.get('price_max_range', None)

        if (float(price['price__max']) % 20.0 != 0):
            price['price__max'] = int(price['price__max'] / 20+1)*20
        if (float(price['price__min']) % 20.0 != 0):
            price['price__min'] = int(price['price__min'] / 20)*20

        if (price['price__min']==0):
            price['price__min'] = 1
            price['price__max'] = price['price__max']+1
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        from django.forms import CheckboxInput, Select, SelectMultiple, NumberInput
        if (min_price_set):
            self.fields['price_min'] = forms.IntegerField(
                widget=RangeInput(valuemin=price['price__min'], valuemax=price['price__max'], value=min_price_set,
                                  step=20))
        else:
            self.fields['price_min'] = forms.IntegerField(widget=RangeInput(valuemin=price['price__min'],valuemax=price['price__max'],value=price['price__min'],step=20))
        if (max_price_set):
            self.fields['price_max'] = forms.IntegerField(
                widget=RangeInput(valuemin=price['price__min'], valuemax=price['price__max'], value=max_price_set,
                                  step=20))
        else:
            self.fields['price_max'] = forms.IntegerField(
            widget=RangeInput(valuemin=price['price__min'], valuemax=price['price__max'], value=price['price__max'], step=20))

        #self.fields['colorchoices'] = forms.MultipleChoiceField(label="Color",required=False,
        #                                          widget=forms.SelectMultiple(attrs={'class': "form-control selectpicker"}),choices=[(m.id,m.name) for m in colorchoices.objects.all()])

        #self.fields['brand'] = forms.MultipleChoiceField(label="Brand",required=False,
        #                                                 widget=forms.SelectMultiple(
        #                                                     attrs={'class': "form-control selectpicker"}),
        #                                                 choices=[(m.id, m.name) for m in brandchoices.objects.all()])
        #self.fields['size'] = forms.MultipleChoiceField(label="Size",required=False,
        #                                                 widget=forms.SelectMultiple(
        #                                                     attrs={'class': "form-control selectpicker"}),
        #                                                 choices=[(m.id, m.name) for m in sizechoices.objects.all()])
        #self.fields['material'] = forms.MultipleChoiceField(label="Material",required=False,
        #                                                widget=forms.SelectMultiple(
        #                                                    attrs={'class': "form-control selectpicker"}),
        #                                                choices=[(m.id, m.name) for m in materialchoices.objects.all()])
        #if (catalogview):
          #  self.fields['color'].initial =



