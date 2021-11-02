

from oscar.core.loading import get_model

from .Widgets import *
from .models import colorchoices,brandchoices,sizechoices,materialchoices
from oscar.apps.dashboard.catalogue.forms import _attr_text_field,_attr_textarea_field,_attr_integer_field,_attr_boolean_field,_attr_float_field,_attr_date_field,_attr_datetime_field,_attr_option_field,_attr_multi_option_field,_attr_entity_field,_attr_numeric_field,_attr_file_field,_attr_image_field
from oscar.apps.dashboard.catalogue.forms import ProductForm as Productformold
from .FormMixins import *


Product = get_model('catalogue', 'Product')


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
        min_price = catalogview.request.GET.get('Price_min', None)

        max_price = catalogview.request.GET.get('Price_max', None)
        super(ProductFilterForm, self).__init__(*args, **kwargs)

        self.fields['price'] = forms.IntegerField(label="",widget=RangeWidget(eav=False,title='Price',valuemin=0,valuemax=100,valuenow=50,initmin=min_price,initmax=max_price))
        self.fields['colorchoices'] = forms.MultipleChoiceField(label="Color",required=False,
                                                  widget=forms.SelectMultiple(attrs={'class': "form-control selectpicker"}),choices=[(m.id,m.name) for m in colorchoices.objects.all()])

        self.fields['brand'] = forms.MultipleChoiceField(label="Brand",required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': "form-control selectpicker"}),
                                                         choices=[(m.id, m.name) for m in brandchoices.objects.all()])
        self.fields['size'] = forms.MultipleChoiceField(label="Size",required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': "form-control selectpicker"}),
                                                         choices=[(m.id, m.name) for m in sizechoices.objects.all()])
        self.fields['material'] = forms.MultipleChoiceField(label="Material",required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': "form-control selectpicker"}),
                                                        choices=[(m.id, m.name) for m in materialchoices.objects.all()])
        #if (catalogview):
          #  self.fields['color'].initial =



