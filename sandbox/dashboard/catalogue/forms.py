from oscar.apps.dashboard.catalogue.forms import ProductForm as Productformold
from django import forms
from oscar.core.loading import get_class, get_classes, get_model
Product = get_model('catalogue', 'Product')
from globalsettings.models import Globalsettings



class ProductForm(Productformold):

    class Meta:
        print("Drin 1234")
        model = Product
        fields = [
            'title', 'upc', 'description', 'is_public', 'is_discountable', 'structure', 'slug', 'meta_title',
            'meta_description','product_tax','color','material','size','brand']
        widgets = {
            'structure': forms.HiddenInput(),
            'meta_description': forms.Textarea(attrs={'class': 'no-widget-init'})
        }
    def __init__(self, *args, **kwargs):
        data = super().__init__(*args, **kwargs)
        if (Globalsettings.kleingewerbe):
            self.fields.pop('product_tax')

        return data

