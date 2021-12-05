from django_filters.views import FilterView
from django.template.loader import render_to_string
#from settings.views import *
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView

from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.apps.catalogue.views import ProductCategoryView as CoreProductCategoryView

from django.views.generic import TemplateView
from oscar.core.loading import get_class

from django.core.paginator import InvalidPage
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic.edit import (

    DeleteView,
    UpdateView,
    CreateView,
)
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from bibliothek.Mixins import SingleFormMixin,Deletesuccessmixin,ListviewMixin
from .forms import *


get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


#Tax CRUD

@method_decorator(login_required, name='dispatch')
class taxlistview(ListviewMixin,ListView):
    model = Tax
    template_name = 'website/standardlistview.html'
    fieldlist = ('id','Taxlabel','Taxvalue' )
    buttons = {
        0: {'url': reverse_lazy('catalogue:taxCreateView'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}


@method_decorator(login_required, name='dispatch')
class taxDeleteView(Deletesuccessmixin,DeleteView):
    model = Tax

@method_decorator(login_required, name='dispatch')
class taxUpdateView(SingleFormMixin, UpdateView):
    model = Tax
    form_class = Taxform
    template_name = 'website/standardformview.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    success_url = reverse_lazy('catalogue:taxlistview')

@method_decorator(login_required, name='dispatch')
class taxCreateView(SingleFormMixin,CreateView):
    model = Tax
    template_name = 'website/standardformview.html'

    success_url = reverse_lazy('catalogue:taxlistview')
    form_class = Taxform

#Brand CRUD

@method_decorator(login_required, name='dispatch')
class brandlistview(ListviewMixin,ListView):
    model = brandchoices
    template_name = 'website/standardlistview.html'
    fieldlist = ('id','name' )
    buttons = {
        0: {'url': reverse_lazy('catalogue:brandCreateView'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}


@method_decorator(login_required, name='dispatch')
class brandDeleteView(Deletesuccessmixin,DeleteView):
    model = brandchoices

@method_decorator(login_required, name='dispatch')
class brandUpdateView(SingleFormMixin, UpdateView):
    model = brandchoices
    form_class = brandform
    template_name = 'website/standardformview.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    success_url = reverse_lazy('catalogue:brandlistview')

@method_decorator(login_required, name='dispatch')
class brandCreateView(SingleFormMixin,CreateView):
    model = brandchoices
    template_name = 'website/standardformview.html'

    success_url = reverse_lazy('catalogue:brandlistview')
    form_class = brandform

#Material CRUD

@method_decorator(login_required, name='dispatch')
class materiallistview(ListviewMixin,ListView):
    model = materialchoices
    template_name = 'website/standardlistview.html'
    fieldlist = ('id','name' )
    buttons = {
        0: {'url': reverse_lazy('catalogue:materialCreateView'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}


@method_decorator(login_required, name='dispatch')
class materialDeleteView(Deletesuccessmixin,DeleteView):
    model = materialchoices

@method_decorator(login_required, name='dispatch')
class materialUpdateView(SingleFormMixin, UpdateView):
    model = materialchoices
    form_class = materialform
    template_name = 'website/standardformview.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    success_url = reverse_lazy('catalogue:materiallistview')

@method_decorator(login_required, name='dispatch')
class materialCreateView(SingleFormMixin,CreateView):
    model = materialchoices
    template_name = 'website/standardformview.html'

    success_url = reverse_lazy('catalogue:materiallistview')
    form_class = materialform


#Color CRUD

@method_decorator(login_required, name='dispatch')
class colorlistview(ListviewMixin,ListView):
    model = colorchoices
    template_name = 'website/standardlistview.html'
    fieldlist = ('id','name' )
    buttons = {
        0: {'url': reverse_lazy('catalogue:colorCreateView'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}


@method_decorator(login_required, name='dispatch')
class colorDeleteView(Deletesuccessmixin,DeleteView):
    model = colorchoices

@method_decorator(login_required, name='dispatch')
class colorUpdateView(SingleFormMixin, UpdateView):
    model = colorchoices
    form_class = colorform
    template_name = 'website/standardformview.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    success_url = reverse_lazy('catalogue:colorlistview')

@method_decorator(login_required, name='dispatch')
class colorCreateView(SingleFormMixin,CreateView):
    model = colorchoices
    template_name = 'website/standardformview.html'

    success_url = reverse_lazy('catalogue:colorlistview')
    form_class = colorform



#Size CRUD

@method_decorator(login_required, name='dispatch')
class sizelistview(ListviewMixin,ListView):
    model = sizechoices
    template_name = 'website/standardlistview.html'
    fieldlist = ('id','name' )
    buttons = {
        0: {'url': reverse_lazy('catalogue:sizeCreateView'), 'awesomefont': "fas fa-plus", 'label': 'Neu'},1: {'url': reverse_lazy('dashboard:index'), 'awesomefont': "fas fa-undo", 'label': 'Dashboard'}}


@method_decorator(login_required, name='dispatch')
class sizeDeleteView(Deletesuccessmixin,DeleteView):
    model = sizechoices

@method_decorator(login_required, name='dispatch')
class sizeUpdateView(SingleFormMixin, UpdateView):
    model = sizechoices
    form_class = Sizeform
    template_name = 'website/standardformview.html'
    success_message = 'Datensatz wurde erfolgreich aktualisiert'
    success_url = reverse_lazy('catalogue:sizelistview')

@method_decorator(login_required, name='dispatch')
class sizeCreateView(SingleFormMixin,CreateView):
    model = sizechoices
    template_name = 'website/standardformview.html'

    success_url = reverse_lazy('catalogue:sizelistview')
    form_class = Sizeform


def getvariant(request):
    if request.method == "GET":
        size = request.GET.get("sizeId",None)
        color = request.GET.get("colorId",None)
        productid = request.GET.get("productid", None)
        changedfield = request.GET.get("changedfield",None)

        #print("Size "+str(size))
        #print("Color "+str(color))
        ##print("Productid "+str(productid))
        #print("Changedfield "+str(changedfield))

        if ((size is None and color is None) or changedfield is None or productid is None):

            return JsonResponse({"error": "Size or Color is None or changedfield is None or Productid is None"}, status=400)
        Variant = None
        if (size is not None and size != "" and color is not None and color != ""):

            Variant = Product.objects.filter(size=size,color=color,parent=productid).first()


            if (Variant):

                context = {'product': Variant,'object': Variant,'request':request}
                if (context['object'].parent):
                    variants = Product.objects.filter(parent=context['object'].parent)
                else:
                    variants = Product.objects.filter(parent=context['object'])
                context['sizes'] = variants.order_by('size').distinct('size')
                context['size'] = str(size)
                context['colors'] = variants.order_by('color').distinct('color').exclude(color__isnull=True)
                context['color'] = str(color)
                #print("Context " + str(context))
                html = render_to_string('oscar/catalogue/partials/productdetailview.html', context, request=request)

                return JsonResponse({"producthtml": html},
                                status=200)


        if (changedfield == 'colorselect'):

            Variant = Product.objects.filter(color=color, parent=productid)
            print("Colorselect "+str(Variant.query))
            if (Variant):
                dict = {}
                for entry in Variant:
                    dict.update({entry.size.id: entry.size.name})

                return JsonResponse({"sizedict": dict},
                                    status=200)
        if (changedfield == 'sizeselect'):

            Variant = Product.objects.filter(size=size, parent=productid)

            if (Variant):
                dict = {}
                for entry in Variant:
                    dict.update({entry.color.id: entry.color.name})

                return JsonResponse({"colordict": dict},
                                    status=200)






    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ProductDetailView(CoreProductDetailView):
    context_object_name = 'product'
    template_name = 'website/product_detail2.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if (context['object'].parent):
            variants = Product.objects.filter(parent=context['object'].parent)
        else:
            variants = Product.objects.filter(parent=context['object'])
        context['sizes'] = variants.order_by('size').distinct('size')
        context['colors'] = variants.order_by('color').distinct('color').exclude(color__isnull=True)

        return context



class ProductCreateUpdateView(CoreProductCreateUpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tax'] = self.product_tax
        context['size'] = self.size
        context['colour'] = self.colour
        #context['recommendations'] = Productrecommendation.objects.filter(recommendation=context['object']).order_by('ranking')
        return context


def getcataloguecontext(self):

        #ctx = {'summary': _("All products"),
        #       'colors': [(m.id, m.name) for m in colorchoices.objects.all()],
        #       'brands': [(m.id, m.name) for m in brandchoices.objects.all()],
        #       'sizes': [(m.id, m.name) for m in sizechoices.objects.all()],
        #       'materials': [(m.id, m.name) for m in materialchoices.objects.all()],
        #       }

        ctx = {'summary': _("All products"),

               }
        productslist = Product.objects.all()

        min_price = self.request.GET.get('price_min_range', None)
        if min_price:
            productslist = productslist.filter(stockrecords__price__gte=min_price)

        max_price = self.request.GET.get('price_max_range', None)
        if max_price:
            productslist = productslist.filter(stockrecords__price__lte=max_price)

        # Nun haben wir die ganzen Varianten. Von diesen vielen Varianten sollen in der LIstenansicht aber nur die Parents angezeigt werden
        list = []
        for entry in productslist:
            if entry.parent is not None:
                if entry.parent not in list:
                    list.append(entry.parent.id)
            else:
                if entry not in list:
                    list.append(entry.id)

        parentproducts = Product.objects.filter(pk__in=list)
        ctx['products'] = parentproducts
        #ctx['Filterform'] = ProductFilterForm(self, initial={'colorchoices': color, 'brand': brand, 'material': material,
        #                                                     'size': size})
        ctx['Filterform'] = ProductFilterForm(self,
                                              )

        #print("Context "+str(ctx))
        return ctx


class ProductCategoryView(CoreProductCategoryView):
    """
    Browse products in a given category
    """
    context_object_name = "products"
    template_name = 'oscar/catalogue/browse.html'

    def get_context_data(self, **kwargs):
        return getcataloguecontext(self)



class CatalogueView(TemplateView):
    """
    Browse all products in the catalogue
    """
    context_object_name = "products"
    template_name = 'oscar/catalogue/browse.html'

    def get(self, request, *args, **kwargs):
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), []
            )
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super().get(request, *args, **kwargs)

    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return getcataloguecontext(self)





